# MUST check for existing logic before adding it — re-use, don't bloat DataService

> **Applies to**: the whole `Telemax2` microservice solution, and **especially** `Telemax.DataService`
> — the high-throughput telemetry engine on the Kafka hot path. Backend-wide MUST-check rule.

**Rule (MUST):** before you add a data lookup, a cache, or a derived value to a service, you MUST first
check whether **another service in the solution already resolves that same fact**, and re-use it instead
of adding a parallel copy. This is mandatory for `DataService`: do **not** widen its metadata caches or
per-message work to carry a value that a downstream consumer (NotificationService, SnapshotService,
Dashboard.Server, …) already has. When in doubt, resolve the value in the service that already owns it.

**Why (the failure it prevents):**
- **DataService is the hot path.** It runs per-vehicle, per-message, thousands of times a second, and
  bulk-loads metadata per batch. Every field added to `VehicleMetadataCache` / `DataStorage` is extra DB
  IO and memory on the critical ingestion loop — paid on every batch, forever, for data that may already
  be sitting in the service that actually needs it.
- **Duplicate resolution drifts.** Two services computing "the company name for this vehicle" from two
  different queries will disagree the day one of them changes (caching, soft-delete filter, company
  hierarchy). One owner = one answer.
- **It's easy to miss** precisely because the added code *works* in isolation — the cost and the drift
  only show up later, in production and in the next person's bug.

---

## Worked example — TLM-3165 `AccountName` (what triggered this rule)

The unified Alert Email V1 needs the company/account name in the footer (`AccountName`).

### ❌ What was done — resolved in DataService and shipped down the wire

```csharp
// Telemax.DataService — commit 0c33f074e
// Widened the hot-path metadata cache just to carry the company name…
VehicleMetadataPatch.CompanyNames        // new
IVehicleMetadataCache.GetCompanyName(id) // new
// …then set it on every alert message:
result.AccountName = _vehicleMetadataCache.GetCompanyName(snapshot.Alert.CompanyId);
```

This added a per-batch company-name load to `DataService` and sent `AccountName` across the pipeline.

### ✅ What the rule asks — re-use the service that already resolves the company

`Telemax.NotificationService` **already** resolves the vehicle's company for alert gating:
`VehicleCompanyProvider` queries the `Companies` table per vehicle (cached, TTL configurable) to read
`CompanyAlertConfiguration`. The company row it already loads carries the **Name**. So the footer's
`AccountName` can be filled **in NotificationService, from the company it already has** — with no new
DataService cache, no new field on the wire, and one authoritative source for "company name".

> Content that is genuinely *computed at the point of production* (e.g. the alert's measured value,
> heading, speed delta — "the template does no maths") correctly belongs in DataService. This rule is
> about **static metadata / look-ups** (company name, vehicle rego, owner) that another service already
> resolves — not about that computed content.

---

## How to check (do this before adding the field)

1. **Name the fact** you need ("company name for a vehicle", "vehicle rego", "owner email").
2. **Grep the other services** for an existing owner before writing a new lookup:
   ```bash
   grep -rniE "companyname|company\.name|Companies|VehicleCompanyProvider|GetCompany" \
     Telemax.NotificationService* Telemax.SnapshotService* Telemax.Dashboard.Server.Services
   ```
   `SnapshotService` (live vehicle state over NATS) and `NotificationService`
   (`VehicleCompanyProvider`) are the two most common places a fact is already resolved.
3. If an owner exists, **resolve/consume it there** and delete the parallel copy. If it does not, add it
   to the service that *owns* the concept — and only add it to `DataService` when `DataService` is the
   sole place the data exists at that point in the pipeline.

## Exceptions

Adding the lookup to `DataService` is acceptable only when **no other running service has the fact at the
time it is needed** (e.g. a value that exists only in the raw message being processed, before any
downstream service has seen the vehicle). When that is the case, state it in the PR description so the
reviewer knows re-use was considered and ruled out — not skipped.
