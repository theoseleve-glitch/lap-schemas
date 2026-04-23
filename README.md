# lap-schemas

Single source of truth for LAP data contracts. Pydantic v2 source → OpenAPI → TS / Swift / Kotlin codegen.

## Layout

```
python/        # Pydantic v2 source. The ONE place schema is defined.
typescript/    # Generated TS types via openapi-typescript. Consumed by lap-webapp.
swift/         # Generated Swift types. Consumed by lap_mobile (iOS, frozen).
kotlin/        # Generated Kotlin types. Consumed by lap-mobile-android.
openapi.json   # Generated OpenAPI 3.1 spec.
Makefile       # Regeneration entrypoints.
```

## Regeneration

Any change to Pydantic models requires regeneration:

```bash
make all  # regenerates openapi.json, then ts/, swift/, kotlin/
```

CI enforces regen — PRs with mutated Pydantic but stale generated artifacts are rejected.

## Versioning

Calver: `YYYY.MM.N`. Bump N on every release, M on the month rollover. Breaking changes require a new major (`vN`) package namespace.

## ADRs

- **ADR-004** — Schema registry design
- **ADR-005** — 7 canonical backend objects (field shapes)
- **ADR-006** — SessionManifest shape
- **ADR-007** — Dual-timestamp TelemetrySample

## Status

Seeded 2026-04-23. Scaffold comes from backend sprint tasks T021-T055.
