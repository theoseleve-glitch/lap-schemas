package com.lap.schemas

/**
 * Marker for the lap-schemas Kotlin module. T027+ will populate this
 * module with generated data classes (SessionManifest, TelemetrySample,
 * etc.); this file exists so T026 has something for consumers to reference
 * when proving the Gradle wiring is live.
 */
object SchemasModule {
    const val NAMESPACE: String = "com.lap.schemas"
}
