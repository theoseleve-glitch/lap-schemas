// Pure Kotlin/JVM library housing generated Kotlin types from the shared
// lap-schemas registry (Pydantic → OpenAPI → Kotlin). Consumed by
// lap-mobile-android via an `include(":schemas")` + projectDir override
// declared in that repo's settings.gradle.kts. Stays JVM-only (not an
// Android library) so the module remains reusable by any JVM consumer
// and doesn't drag in the Android SDK.

plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.serialization)
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
    compilerOptions {
        jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
    }
}

dependencies {
    implementation(libs.kotlinx.serialization.json)
    testImplementation(libs.junit)
}
