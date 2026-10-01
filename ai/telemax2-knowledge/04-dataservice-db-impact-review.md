# MUST review migrations and queries before a change touches DataService

> **Applies to**: any `Telemax2` change whose logic touches `Telemax.DataService*` (handlers, producers,
> `DataStorage`, `RecordWriter`, `VehicleMetadataCache`, record entities) **or** a table that DataService
> reads/writes — records / positions / routes / alerts (TimescaleDB hypertables), `vehicle_handler_states`,
> `Vehicles`, `Companies`, alert snapshots, geofences. Also any EF migration in `Telemax.Shared.ClientDb`
> that alters one of those tables.

**Rule (MUST):** before implementing, **review every migration and every query the change adds or alters**
for database impact, and write the result into the plan (a `## DB impact` section) for the user to
confirm. No migration or new DataService query lands without that review. All queries follow
[`shared-be/01` — no N+1](../shared-be/01-avoid-n-plus-1-queries.md); complex ones follow
[`shared-be/04` — brainstorm + confirm](../shared-be/04-complex-queries-brainstorm-first.md).

**Why (the failure it prevents):** DataService is the ingestion hot path. It consumes Kafka in batches of up
to 1000 messages / 1 s, bulk-loads metadata per batch (`GetVehicleMetadataPatchAsync`) and writes every
record with **COPY BINARY** into a Postgres/TimescaleDB that **every other service shares**. So:

- one extra query per batch is paid thousands of times an hour, forever; one per message is an outage;
- a migration that locks a hypertable or rewrites a large table **stalls ingestion** — Kafka lag grows,
  alerts arrive late, and Dashboard/Reports slow down on the same DB;
- `RecordWriter` builds the COPY column list from the record type — a renamed/dropped/retyped column fails
  **the whole batch**, not one row; during a rolling deploy the *old* DataService build is still writing;
- `vehicle_handler_states` holds each handler's JSON state — breaking its shape silently resets detection
  state for every vehicle on restart.

---

## Migration review — check each item

| Check | Risk if missed | Safe pattern |
|---|---|---|
| **Which DB the migration hits** | Applying to the wrong host | EF reads `Telemax.Shared.ClientDb/design-time-factory-settings.json`, **not** appsettings — verify the host first |
| **Table size** (`pg_total_relation_size`, row count, is it a hypertable?) | Long lock on a large table | Anything on a hypertable / >1M rows gets an explicit lock + duration estimate in the plan |
| **`CREATE INDEX`** on a large/live table | `SHARE` lock blocks all writes (COPY) for the build | `migrationBuilder.Sql("CREATE INDEX CONCURRENTLY IF NOT EXISTS …", suppressTransaction: true)` — EF's `CreateIndex` is not concurrent. On hypertables check TimescaleDB support (`WITH (timescaledb.transaction_per_chunk)`) |
| **Add column** | Table rewrite / failed migration | Nullable, or a constant default (no rewrite on PG 11+). Never `NOT NULL` without default on existing rows; never a volatile default |
| **Alter column type / rename / drop** | Full rewrite + `ACCESS EXCLUSIVE`; COPY batches from the old build fail | Expand → migrate → contract across releases: add new column, dual-write, backfill, switch reads, drop later |
| **Data backfill / `UPDATE` in a migration** | Huge transaction, bloat, long locks | Keep it out of the migration — a batched, resumable job (e.g. 5–10k rows per batch) |
| **Compressed hypertable chunks** | DDL rejected or very slow on compressed chunks | Check compression policy before altering; plan decompress/recompress if needed |
| **Backward compatibility** | Old build crashes between migrate and deploy | Migration must be safe with the *currently running* DataService still writing |
| **`Down()`** | No rollback path | Real inverse, or state explicitly that the migration is forward-only and why |
| **Generated SQL** | EF emits something different from what you think | `dotnet ef migrations script <prev> <new>` and read the SQL before applying |

## Query review — check each item

- **Where it runs**: per message ✗ · per vehicle per batch ✗ (almost always) · once per batch ✓ ·
  startup / cache refresh ✓. Say which in the plan.
- **No N+1** — batch by the batch's vehicle ids in one query, never inside the per-vehicle loop.
- **Index use** — the predicate hits an existing index (name it) or the plan adds one (then the migration
  review above applies). Show `ToQueryString()` and, for large tables, `EXPLAIN (ANALYZE, BUFFERS)` from a
  realistic DB.
- **Time-bounded** on hypertables — always constrain the time column so chunk exclusion works.
- **Projection only** — `Select` the columns you need, `AsNoTracking()`; never load whole entities/tables
  into the batch loop.
- **Re-use first** — does another service or the existing metadata patch already have this fact?
  ([`01`](./01-reuse-existing-service-logic.md)).
- **Writes** — new record types must map cleanly to COPY BINARY columns; handler-state changes keep the
  existing short JSON property names.

---

## ❌ Don't

```csharp
// Migration: blocking index on a hypertable, plus a backfill in the same transaction
migrationBuilder.CreateIndex("IX_AlertRecords_CompanyId", "AlertRecords", "CompanyId");
migrationBuilder.Sql("UPDATE \"AlertRecords\" SET \"CompanyId\" = …");     // whole table, one tx

// Handler: a lookup per vehicle per batch
var name = await _db.Companies.Where(c => c.Id == vehicle.CompanyId).Select(c => c.Name).FirstAsync(ct);
```

## ✅ Do

```csharp
migrationBuilder.Sql(
    "CREATE INDEX CONCURRENTLY IF NOT EXISTS \"IX_AlertRecords_CompanyId\" ON \"AlertRecords\" (\"CompanyId\");",
    suppressTransaction: true);
// backfill → separate batched job, not the migration

// Metadata resolved once per batch inside GetVehicleMetadataPatchAsync (one IN-query for all vehicle ids),
// or — better — owned by the downstream service that already has it.
```

## Plan template — `## DB impact`

```markdown
## DB impact
- Migrations: <name> — tables touched, size/hypertable?, lock taken, est. duration, concurrent?, backward-compatible?, Down()
- Queries: <where it runs (per batch / startup)>, round-trips, index used, rows scanned vs returned
- Generated SQL / EXPLAIN: <attached or summarised>
- Deploy order: migrate → deploy DataService → … (or "no migration")
```

**Wait for the user's confirmation of this section before implementing.**
