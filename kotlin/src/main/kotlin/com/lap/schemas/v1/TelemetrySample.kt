package com.lap.schemas.v1

/**
 * Single captured sample, mirroring `lap_schemas.v1.telemetry_sample.TelemetrySample`.
 *
 * ADR-007 (timestamp normalization) is the reason this type carries two
 * timestamps. Capture clients ship the raw sensor reading verbatim; the
 * ingestion pipeline (ADR-012) fills [tCanonicalNs] server-side. On the
 * mobile capture path we set [tCanonicalNs] equal to [tSourceNs] until
 * the server aligns; clients do NOT pre-fuse.
 *
 * [tSourceClock] values come from the locked Python `SourceClock` literal:
 * `"gnss"`, `"coremotion"`, `"racebox_gnss"`, `"irsdk_tick"`,
 * `"acc_shmem"`, `"device_monotonic"`. Kept as String here; promoted to
 * a typed enum when codegen arrives.
 *
 * [channels] is a free-form `Map<String, Double>` — the set of channel
 * names is defined by the server ingestion contract, not by the client.
 */
data class TelemetrySample(
    val tSourceNs: Long,
    val tCanonicalNs: Long,
    val tSourceClock: String,
    val channels: Map<String, Double> = emptyMap(),
)
