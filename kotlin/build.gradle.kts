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

// Temporarily excludes the codegen-authored `generated/` package from
// compilation: the backend sprint (lap-schemas T051) emits Kotlin that
// references java.math.BigDecimal without a @Serializable serializer,
// which breaks the kotlinx-serialization compiler plugin and blocks
// every downstream mobile task that depends on :schemas. Mobile sprint
// consumers stay on the hand-typed `v1/` stubs (T027–T039) until
// generated/ is fixed upstream with either @Contextual + a
// BigDecimalSerializer or @file:UseSerializers. Revert when green.
tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
    exclude("com/lap/schemas/generated/**")
}

dependencies {
    implementation(libs.kotlinx.serialization.json)
    testImplementation(libs.junit)
}
