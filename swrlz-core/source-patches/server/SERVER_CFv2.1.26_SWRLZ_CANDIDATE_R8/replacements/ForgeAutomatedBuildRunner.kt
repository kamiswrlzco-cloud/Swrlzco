package sh.swrlz.nodehost.forge

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

data class ForgeAutomatedBuildResult(
    val upload: GitHubForgeClient.UploadResult,
    val discovery: ForgeProjectDiscovery,
    val activeToken: String,
    val connectedLogin: String,
) {
    val candidates: List<ForgeVerifiedSourceCandidate> get() = discovery.candidates
    val effectiveTarget: ForgeBuildTarget get() = discovery.effectiveTarget
}

/** User-initiated Downloads inbox -> verified package set -> GitHub -> build-watch conveyor. */
object ForgeAutomatedBuildRunner {
    suspend fun run(
        context: Context,
        target: ForgeBuildTarget,
        owner: String,
        repository: String,
        branch: String,
        currentToken: String,
        oauthClientId: String,
        workflowId: String,
        destinationDirectory: String,
        clientSourceDirectory: String,
        serverSourceDirectory: String,
        autoRoute: Boolean,
        sourceZipGuard: Boolean,
        sourceTransportMode: GitHubForgeClient.SourceTransportMode,
        forgeActor: String,
        onProgress: suspend (Int, String) -> Unit = { _, _ -> },
    ): ForgeAutomatedBuildResult = withContext(Dispatchers.IO) {
        require(target in setOf(ForgeBuildTarget.ASK, ForgeBuildTarget.CLIENT, ForgeBuildTarget.SERVER, ForgeBuildTarget.BOTH)) {
            "Downloads inbox upload requires ASK, CLIENT, SERVER, or BOTH."
        }
        onProgress(1, "Scanning configured Downloads inbox for CLIENT/SERVER source packages…")
        val discovery = ForgeSourceResolver.discoverDownloads(context, target)
        require(discovery.ready) {
            discovery.conflicts.joinToString(" ").ifBlank {
                "No complete verified CLIENT or SERVER source package set was found in the configured Downloads inbox."
            }
        }
        val candidates = discovery.candidates
        val effectiveTarget = discovery.effectiveTarget
        fun repositoryLane(candidate: ForgeVerifiedSourceCandidate): String = when (candidate.component.uppercase()) {
            "CLIENT" -> clientSourceDirectory.trim().ifBlank { "SOURCES/CLIENT" }
            "SERVER" -> serverSourceDirectory.trim().ifBlank { "SOURCES/SERVER" }
            else -> destinationDirectory.trim()
        }
        val descriptions = candidates.map { it to it.operatorDescription(repositoryLane(it)) }
        onProgress(
            6,
            "AUTO-DETECTED ${effectiveTarget.name} · " + descriptions.joinToString(" | ") { it.second },
        )
        descriptions.forEach { (candidate, description) ->
            ForgeBuildLedger.record(
                context = context,
                state = ForgeLedgerState.SOURCE_FOUND,
                component = candidate.component,
                sourceName = candidate.displayName,
                sourceSha256 = candidate.sha256,
                sourceVersion = candidate.version,
                sourceRevision = candidate.revision,
                versionCode = candidate.versionCode,
                detail = "Downloads inbox selected: $description",
            )
            ForgeBuildLedger.record(
                context = context,
                state = ForgeLedgerState.VERIFIED,
                component = candidate.component,
                sourceName = candidate.displayName,
                sourceSha256 = candidate.sha256,
                sourceVersion = candidate.version,
                sourceRevision = candidate.revision,
                versionCode = candidate.versionCode,
                detail = "Verified source and companion package: $description",
            )
        }
        val files = ForgeSourceResolver.asLocalFiles(candidates, discovery.evidenceBundle)
        val expectedPackageFiles = candidates.sumOf { it.stagedFileCount }
        val expectedTotal = expectedPackageFiles + if (discovery.evidenceBundle != null) 1 else 0
        require(files.size == expectedTotal) {
            "Verified package conversion failed: expected $expectedTotal staged files, found ${files.size}."
        }
        candidates.forEach { candidate ->
            require(
                (candidate.metadataBundle != null && candidate.checksum == null && candidate.manifest == null) ||
                    (candidate.metadataBundle == null && candidate.checksum != null && candidate.manifest != null)
            ) { "${candidate.component} package evidence is mixed or incomplete." }
        }
        if (sourceZipGuard) {
            val rejected = files.filter { GitHubForgeClient.isProtectedSourceZip(it.displayName) }
                .map { GitHubForgeClient.inspectSourceZip(context, it) }
                .firstOrNull { !it.valid }
            require(rejected == null) { rejected?.message ?: "Source ZIP guard rejected the source." }
        }
        val pairValidation = GitHubForgeClient.validateSourcePairs(context, files)
        require(pairValidation.valid) { pairValidation.message }
        onProgress(
            12,
            "VERIFIED FOR UPLOAD · " + descriptions.joinToString(" | ") { it.second } +
                (discovery.evidenceBundle?.name?.let { " · evidence $it" } ?: ""),
        )

        val credential = GitHubCredentialLifecycle.ensureValid(
            context = context,
            oauthClientId = oauthClientId,
            owner = owner,
            repository = repository,
            branch = branch,
            currentToken = currentToken,
        )
        val logId = ForgeUploadLogStore.startSession(
            context,
            "FIND DOWNLOADS & FORGE VERIFIED SET · ${effectiveTarget.name} · " +
                candidates.joinToString(" + ") { it.displayName },
        )
        val sourceSummary = candidates.joinToString(" + ") {
            "${it.component} ${it.displayName} CFv${it.version} ${it.revision} VC${it.versionCode}"
        }
        val request = GitHubForgeClient.UploadRequest(
            owner = owner,
            repository = repository,
            branch = branch,
            destinationDirectory = destinationDirectory,
            commitMessage = "forge: upload verified $sourceSummary",
            token = credential.token,
            files = files,
            workflowId = workflowId,
            dispatchWorkflow = workflowId.isNotBlank(),
            autoRouteSourcePackages = autoRoute,
            clientSourceDirectory = clientSourceDirectory,
            serverSourceDirectory = serverSourceDirectory,
            forgeActor = forgeActor,
            logSessionId = logId,
            sourceTransportMode = sourceTransportMode,
            onProgress = onProgress,
        )
        val result = try {
            GitHubForgeClient.upload(context, request)
        } catch (failure: Throwable) {
            val description = descriptions.joinToString(" | ") { it.second }
            ForgeUploadLogStore.appendFailure(context, logId, "AUTOMATED_BUILD_FAILURE · $description", failure)
            ForgeUploadLogStore.finish(context, logId, "FAILED · $description")
            throw failure
        }

        descriptions.forEach { (candidate, description) ->
            ForgeBuildLedger.record(
                context = context,
                state = ForgeLedgerState.UPLOADED,
                transactionId = result.transactionId,
                component = candidate.component,
                sourceName = candidate.displayName,
                sourceSha256 = candidate.sha256,
                sourceVersion = candidate.version,
                sourceRevision = candidate.revision,
                versionCode = candidate.versionCode,
                commitSha = result.commitSha,
                detail = "Repository upload verified: $description",
            )
            ForgeBuildLedger.record(
                context = context,
                state = ForgeLedgerState.BUILD_REQUESTED,
                transactionId = result.transactionId,
                component = candidate.component,
                sourceName = candidate.displayName,
                sourceSha256 = candidate.sha256,
                sourceVersion = candidate.version,
                sourceRevision = candidate.revision,
                versionCode = candidate.versionCode,
                commitSha = result.commitSha,
                detail = (if (result.workflowDispatched) "workflow_dispatch accepted" else "Push/router build watch armed") +
                    ": build ${candidate.component} APK from $description",
            )
        }
        if (result.repositoryChanged || result.workflowDispatched) {
            val now = System.currentTimeMillis()
            descriptions.forEach { (candidate, description) ->
                ForgeBuildWatchStore.add(
                    context,
                    ForgeBuildWatch(
                        owner = owner.trim(),
                        repository = repository.trim(),
                        branch = branch.trim(),
                        commitSha = result.commitSha,
                        transactionId = result.transactionId,
                        createdAtMillis = now,
                        component = candidate.component,
                        sourceName = candidate.displayName,
                        sourceSha256 = candidate.sha256,
                        sourceVersion = candidate.version,
                        sourceRevision = candidate.revision,
                        versionCode = candidate.versionCode,
                        sourceDescription = description,
                    ),
                )
            }
        }
        val completedDescription = descriptions.joinToString(" | ") { it.second }
        ForgeUploadLogStore.finish(
            context,
            logId,
            "SUCCESS · commit ${result.commitSha} · $completedDescription",
        )
        ForgeAutomatedBuildResult(result, discovery, credential.token, credential.login)
    }
}
