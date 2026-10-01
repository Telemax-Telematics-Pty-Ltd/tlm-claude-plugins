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
| [02 — Company hierarchy visibility](02-company-hierarchy-visibility.md) | A user assigned to any company sees that company AND all its descendants; suspension cascades down the tree. Every "companies for a user" endpoint MUST return the same set as the login path. |
| [03 — Dashboard FE naming](03-dashboard-fe-naming.md) | Blazor dashboard client: every component of a screen family carries one feature prefix (e.g. `VehicleDetail*`); only routed files end in `Page` and carry `@page`. |
| [04 — DataService DB impact review](04-dataservice-db-impact-review.md) | Any change touching DataService (or the tables it reads/writes) MUST review every migration and query for DB impact — locks, index builds, rewrites, COPY BINARY compatibility, per-batch cost — and get the `## DB impact` plan section confirmed first. |
| [05 — Dashboard dates in the user's timezone](05-dashboard-dates-user-timezone.md) | Blazor dashboard: every date/time is converted to the user's timezone (user settings) and formatted with their date format, with **no** zone label. Zone labels belong to HTML emails and other off-dashboard messages only. |
| [Loading states (shared-fe/03)](../shared-fe/03-component-patterns.md) | Dashboard UI too: every async region (first load, filter/range change, refresh, Load more, photos) shows a revamp `Skeleton` in the content's shape, and loading looks different from failed. |
