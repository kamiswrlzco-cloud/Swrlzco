import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
    id("org.jetbrains.kotlin.plugin.serialization")
    id("com.google.dagger.hilt.android")
    id("com.google.devtools.ksp")
}

val localProps = Properties().apply {
    val file = rootProject.file("local.properties")
    if (file.exists()) load(file.reader())
}

fun swrlzSigningValue(key: String): String =
    ((localProps[key] as String?) ?: System.getenv(key)).orEmpty().trim()

val swrlzKeystoreFile = swrlzSigningValue("SWRLZ_DEV_KEYSTORE_FILE")
val swrlzKeystorePassword = swrlzSigningValue("SWRLZ_DEV_KEYSTORE_PASSWORD")
val swrlzKeyAlias = swrlzSigningValue("SWRLZ_DEV_KEY_ALIAS")
val swrlzKeyPassword = swrlzSigningValue("SWRLZ_DEV_KEY_PASSWORD")
val swrlzSigningReady = listOf(
    swrlzKeystoreFile,
    swrlzKeystorePassword,
    swrlzKeyAlias,
    swrlzKeyPassword,
).all(String::isNotBlank)

android {
    namespace = "sh.swrlz.nodehost"
    compileSdk = 34

    signingConfigs {
        if (swrlzSigningReady) {
            create("swrlzDev") {
                storeFile = rootProject.file(swrlzKeystoreFile)
                storePassword = swrlzKeystorePassword
                keyAlias = swrlzKeyAlias
                keyPassword = swrlzKeyPassword
            }
        }
    }

    defaultConfig {
        applicationId = "sh.swrlz.nodehost"
        minSdk = 24
        targetSdk = 34
        versionCode = 91
        versionName = "2.1.26-forge-package-namespace-fix-r8"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }


    buildTypes {
        debug {
            if (swrlzSigningReady) signingConfig = signingConfigs.getByName("swrlzDev")
        }
        release {
            isMinifyEnabled = false
            signingConfig = if (swrlzSigningReady) signingConfigs.getByName("swrlzDev") else signingConfigs.getByName("debug")
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
        isCoreLibraryDesugaringEnabled = true
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(project(":theme-contract"))
    implementation(project(":profile-contract"))
    implementation(project(":provider-contract"))
    implementation(project(":command-contract"))
    implementation(project(":ai-runtime-contract"))
    implementation(project(":model-rack-contract"))

    implementation("androidx.core:core-ktx:1.13.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.4")
    implementation("androidx.activity:activity-compose:1.9.2")
    implementation(platform("androidx.compose:compose-bom:2024.06.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.navigation:navigation-compose:2.7.4")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.4")
    implementation("androidx.hilt:hilt-navigation-compose:1.0.0")
    implementation("com.google.dagger:hilt-android:2.48.1")
    ksp("com.google.dagger:hilt-compiler:2.48.1")
    implementation("androidx.room:room-runtime:2.6.1")
    implementation("androidx.room:room-ktx:2.6.1")
    ksp("androidx.room:room-compiler:2.6.1")
    implementation("androidx.datastore:datastore-preferences:1.0.0")
    implementation("androidx.documentfile:documentfile:1.0.1")
    implementation("androidx.work:work-runtime-ktx:2.7.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.9.0")
    // INT-AI-040B: open MIT Android wrapper around pinned llama.cpp; model weights remain external.
    implementation("dev.ffmpegkit-maintained:llama-android:0.1.1")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.1")
    implementation("io.ktor:ktor-client-core:2.3.12")
    implementation("io.ktor:ktor-client-okhttp:2.3.12")
    implementation("io.ktor:ktor-client-content-negotiation:2.3.12")
    implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.12")
    implementation("io.ktor:ktor-client-websockets:2.3.12")
    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.2")
    implementation("androidx.security:security-crypto:1.1.0")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.9.0")
    androidTestImplementation("androidx.test.ext:junit:1.13.2")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.3.1")
    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
