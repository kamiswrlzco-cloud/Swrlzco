package sh.swrlz.nodehost.forge

import android.content.Context

/** Polls durable Forge source watches and saves each successfully built actual APK once. */
object ForgeBuildMonitor {
    suspend fun pollOnce(context: Context) {
        val appContext = context.applicationContext
        val token = ServerForgeSecretStore.githubToken(appContext)
        if (token.isBlank()) return

        val watches = ForgeBuildWatchStore.pending(appContext)
        if (watches.isEmpty()) return

        val grouped = watches.groupBy { Triple(it.owner, it.repository, it.branch) }
        for ((target, targetWatches) in grouped) {
            val (owner, repository, branch) = target
            val runs = runCatching {
                GitHubForgeClient.listWorkflowRuns(owner, repository, branch, token)
            }.getOrNull() ?: continue

            for (watch in targetWatches) {
                val commitRuns = runs.filter { run ->
                    run.headSha.equals(watch.commitSha, ignoreCase = true) && isArtifactBuild(run)
                }
                val matchingRun = commitRuns.firstOrNull { runMatchesComponent(it, watch.component) }
                    ?: commitRuns.firstOrNull()
                    ?: continue
                if (!matchingRun.status.equals("completed", ignoreCase = true)) {
                    if (!ForgeBuildLedger.hasState(appContext, watch.transactionId, ForgeLedgerState.RUNNING, matchingRun.id)) {
                        ForgeBuildLedger.record(
                            context = appContext,
                            state = ForgeLedgerState.RUNNING,
                            transactionId = watch.transactionId,
                            runId = matchingRun.id,
                            component = watch.component,
                            sourceName = watch.sourceName,
                            sourceSha256 = watch.sourceSha256,
                            sourceVersion = watch.sourceVersion,
                            sourceRevision = watch.sourceRevision,
                            versionCode = watch.versionCode.takeIf { it > 0 },
                            commitSha = watch.commitSha,
                            detail = "${matchingRun.name} · ${matchingRun.status} · building ${watch.sourceDescription.ifBlank { watch.sourceName }}",
                        )
                    }
                    continue
                }
                val completed = matchingRun
                val conclusion = completed.conclusion ?: "unknown"
                if (!ForgeBuildWatchStore.markOutcomeNotified(appContext, completed.id, conclusion, watch.component)) {
                    ForgeBuildWatchStore.complete(appContext, watch)
                    continue
                }

                val allArtifacts = if (conclusion.equals("success", ignoreCase = true)) {
                    runCatching { GitHubForgeClient.listArtifacts(owner, repository, completed.id, token).filter { !it.expired } }
                        .getOrDefault(emptyList())
                } else emptyList()
                val availableArtifacts = selectArtifacts(allArtifacts, watch)
                val buildDescription = watch.sourceDescription.ifBlank {
                    "${watch.component.ifBlank { "ANDROID" }} source ${watch.sourceName} · SHA-256 ${watch.sourceSha256}"
                }

                ForgeBuildLedger.record(
                    context = appContext,
                    state = if (conclusion.equals("success", ignoreCase = true)) ForgeLedgerState.BUILD_SUCCEEDED else ForgeLedgerState.BUILD_FAILED,
                    transactionId = watch.transactionId,
                    runId = completed.id,
                    component = watch.component,
                    sourceName = watch.sourceName,
                    sourceSha256 = watch.sourceSha256,
                    sourceVersion = watch.sourceVersion,
                    sourceRevision = watch.sourceRevision,
                    versionCode = watch.versionCode.takeIf { it > 0 },
                    commitSha = watch.commitSha,
                    detail = "${completed.name} · $conclusion · $buildDescription",
                )

                if (conclusion.equals("success", ignoreCase = true) && ForgeAutomationPreferences.autoDownloadArtifact(appContext)) {
                    if (availableArtifacts.isEmpty()) {
                        ForgeBuildLedger.record(
                            context = appContext,
                            state = ForgeLedgerState.BUILD_SUCCEEDED,
                            transactionId = watch.transactionId,
                            runId = completed.id,
                            component = watch.component,
                            sourceName = watch.sourceName,
                            sourceSha256 = watch.sourceSha256,
                            sourceVersion = watch.sourceVersion,
                            sourceRevision = watch.sourceRevision,
                            versionCode = watch.versionCode.takeIf { it > 0 },
                            commitSha = watch.commitSha,
                            detail = "Build succeeded, but no unambiguous ${watch.component} APK artifact matched $buildDescription",
                        )
                    }
                    availableArtifacts.forEach { artifact ->
                        runCatching {
                            val artifactZip = GitHubForgeClient.downloadArtifact(owner, repository, artifact.id, token)
                            val extracted = ForgeArtifactExtractor.extractApk(artifact.name, artifactZip, watch.component)
                            val savedApk = ForgeArtifactStore.saveApk(appContext, extracted.displayName, extracted.bytes)
                            require(savedApk.sha256.equals(extracted.sha256, ignoreCase = true)) {
                                "Saved APK SHA-256 differs from extracted APK SHA-256."
                            }
                            ForgeBuildLedger.record(
                                context = appContext,
                                state = ForgeLedgerState.ARTIFACT_DOWNLOADED,
                                transactionId = watch.transactionId,
                                runId = completed.id,
                                component = watch.component,
                                sourceName = watch.sourceName,
                                sourceSha256 = watch.sourceSha256,
                                sourceVersion = watch.sourceVersion,
                                sourceRevision = watch.sourceRevision,
                                versionCode = watch.versionCode.takeIf { it > 0 },
                                commitSha = watch.commitSha,
                                artifactName = savedApk.displayName,
                                artifactSha256 = savedApk.sha256,
                                artifactSizeBytes = savedApk.sizeBytes,
                                localUri = savedApk.uri.toString(),
                                detail = "Actual APK extracted from GitHub artifact ${artifact.name} entry ${extracted.artifactEntry}; built from $buildDescription",
                            )
                            ForgeBuildLedger.record(
                                context = appContext,
                                state = ForgeLedgerState.INSTALL_PENDING,
                                transactionId = watch.transactionId,
                                runId = completed.id,
                                component = watch.component,
                                sourceName = watch.sourceName,
                                sourceSha256 = watch.sourceSha256,
                                sourceVersion = watch.sourceVersion,
                                sourceRevision = watch.sourceRevision,
                                versionCode = watch.versionCode.takeIf { it > 0 },
                                commitSha = watch.commitSha,
                                artifactName = savedApk.displayName,
                                artifactSha256 = savedApk.sha256,
                                artifactSizeBytes = savedApk.sizeBytes,
                                localUri = savedApk.uri.toString(),
                                detail = "Verified APK saved under Download/${ForgeAutomationPreferences.projectDirectoryName(appContext)}/apk; installation remains explicit",
                            )
                            if (ForgeAutomationPreferences.keepArtifactZip(appContext)) {
                                val zipName = if (artifact.name.endsWith(".zip", true)) artifact.name else "${artifact.name}.zip"
                                ForgeArtifactStore.saveArtifactZip(appContext, zipName, artifactZip)
                            }
                        }.onFailure { failure ->
                            ForgeBuildLedger.record(
                                context = appContext,
                                state = ForgeLedgerState.BUILD_SUCCEEDED,
                                transactionId = watch.transactionId,
                                runId = completed.id,
                                component = watch.component,
                                sourceName = watch.sourceName,
                                sourceSha256 = watch.sourceSha256,
                                sourceVersion = watch.sourceVersion,
                                sourceRevision = watch.sourceRevision,
                                versionCode = watch.versionCode.takeIf { it > 0 },
                                commitSha = watch.commitSha,
                                detail = "Build succeeded for $buildDescription; automatic APK extraction/save failed: ${failure.message ?: failure::class.java.simpleName}",
                            )
                        }
                    }
                } else if (!conclusion.equals("success", ignoreCase = true) && ForgeAutomationPreferences.autoDownloadFailureLogs(appContext)) {
                    runCatching {
                        val bytes = GitHubForgeClient.downloadWorkflowLogs(owner, repository, completed.id, token)
                        val safeWorkflow = completed.name.replace(Regex("[^A-Za-z0-9._-]+"), "_")
                        val safeComponent = watch.component.ifBlank { "ANDROID" }
                        val saved = ForgeArtifactStore.saveFailureLogs(
                            appContext,
                            "workflow_${completed.id}_${safeComponent}_${safeWorkflow}_logs.zip",
                            bytes,
                        )
                        ForgeBuildLedger.record(
                            context = appContext,
                            state = ForgeLedgerState.LOGS_DOWNLOADED,
                            transactionId = watch.transactionId,
                            runId = completed.id,
                            component = watch.component,
                            sourceName = watch.sourceName,
                            sourceSha256 = watch.sourceSha256,
                            sourceVersion = watch.sourceVersion,
                            sourceRevision = watch.sourceRevision,
                            versionCode = watch.versionCode.takeIf { it > 0 },
                            commitSha = watch.commitSha,
                            artifactName = saved.displayName,
                            artifactSha256 = saved.sha256,
                            artifactSizeBytes = saved.sizeBytes,
                            localUri = saved.uri.toString(),
                            detail = "Automatic failed-workflow logs for $buildDescription",
                        )
                    }.onFailure { failure ->
                        ForgeBuildLedger.record(
                            context = appContext,
                            state = ForgeLedgerState.BUILD_FAILED,
                            transactionId = watch.transactionId,
                            runId = completed.id,
                            component = watch.component,
                            sourceName = watch.sourceName,
                            sourceSha256 = watch.sourceSha256,
                            sourceVersion = watch.sourceVersion,
                            sourceRevision = watch.sourceRevision,
                            versionCode = watch.versionCode.takeIf { it > 0 },
                            commitSha = watch.commitSha,
                            detail = "Build failed for $buildDescription; automatic log save failed: ${failure.message ?: failure::class.java.simpleName}",
                        )
                    }
                }

                ForgeEventNotifier.workflowCompleted(
                    context = appContext,
                    runId = completed.id,
                    workflowName = "${completed.name} · ${watch.component.ifBlank { "ANDROID" }} · ${watch.sourceName}",
                    conclusion = completed.conclusion,
                    artifactCount = availableArtifacts.size,
                    commitSha = watch.commitSha,
                    transactionId = watch.transactionId,
                )
                ForgeBuildWatchStore.complete(appContext, watch)
            }
        }
    }

    private fun runMatchesComponent(run: GitHubForgeClient.WorkflowRun, component: String): Boolean {
        if (component.isBlank()) return true
        val identity = "${run.name} ${run.displayTitle}".lowercase()
        return identity.contains(component.lowercase())
    }

    private fun selectArtifacts(
        artifacts: List<GitHubForgeClient.Artifact>,
        watch: ForgeBuildWatch,
    ): List<GitHubForgeClient.Artifact> {
        if (artifacts.isEmpty()) return emptyList()
        val component = watch.component.lowercase()
        val sourceStem = watch.sourceName.substringBeforeLast('.').lowercase()
        val exact = artifacts.filter { artifact ->
            val name = artifact.name.lowercase()
            (component.isNotBlank() && name.contains(component)) ||
                (sourceStem.isNotBlank() && name.contains(sourceStem))
        }
        return when {
            exact.isNotEmpty() -> exact
            artifacts.size == 1 -> artifacts
            else -> emptyList()
        }
    }

    private fun isArtifactBuild(run: GitHubForgeClient.WorkflowRun): Boolean {
        val identity = "${run.name} ${run.displayTitle}".lowercase()
        return listOf("apk", "artifact", "build", "router", "assemble").any(identity::contains)
    }
}
