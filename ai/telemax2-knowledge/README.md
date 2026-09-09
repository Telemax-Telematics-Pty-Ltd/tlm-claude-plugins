# Telemax2 Knowledge — MUST-check rules

> **Applies to**: the `Telemax2` .NET microservice solution (DataService, NotificationService,
> SnapshotService, GeoDataService, Dashboard.Server, RemindersService, gateways, …).

These are **MUST-check** rules: things a contributor (human or AI) is required to verify *before*
writing code in this solution, because getting them wrong is expensive and easy to miss. They are not
style preferences — they are guard-rails specific to how Telemax2 is wired (a multi-service telemetry
pipeline where the same fact is often already resolved somewhere downstream).

| Rule | One-line |
|------|----------|
| [01 — Re-use existing service logic; don't bloat DataService](01-reuse-existing-service-logic.md) | Before adding data/lookup logic to a service (especially the hot `DataService` path), MUST check whether another service already owns that data and re-use it. |
