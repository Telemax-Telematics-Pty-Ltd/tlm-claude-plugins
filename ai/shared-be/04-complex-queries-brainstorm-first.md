# Complex Queries — Brainstorm, Then Confirm, Then Write (Shared Backend)

> **Applies to**: any backend change that adds or reshapes a non-trivial database query — EF Core (.NET),
> Prisma (Next.js API), TypeORM, raw SQL / Dapper. Cross-stack backend rule, the backend counterpart to
> `ai/shared-fe/`. Companion of [`01-avoid-n-plus-1-queries.md`](./01-avoid-n-plus-1-queries.md).

**Rule (MUST):** before writing a **complex** query, stop and **brainstorm at least two query shapes**,
compare them, and **get the user's confirmation on the chosen approach** — *then* implement. Never ship a
complex query as the first shape that compiled. A simple query (single table, filtered by an indexed key,
small bounded result) needs no ceremony.

**And always (no exception): no N+1.** Every query you write — simple or complex — loads a collection's
related data in one round-trip (see [`01`](./01-avoid-n-plus-1-queries.md)). A query per item inside a loop
is a defect, not a style choice.

**Why (the failure it prevents):** complex queries are where the ORM silently does the expensive thing —
a `GroupBy` that EF evaluates as N sub-queries, an `Include` chain that explodes into a cartesian product,
a `Contains` over 20,000 ids, a filter on a non-indexed column of a multi-million-row table, a recursive
walk issued per node. They pass review because the C#/TS reads cleanly and pass tests because the test DB
has 10 rows. The cost shows up in production as a slow endpoint, a pegged DB CPU, or a lock held during the
busy hour — on a database shared by every service. A five-minute comparison of shapes up front is cheaper
than any of those.

---

## What counts as "complex" (any one is enough)

- joins / `Include`s across **3+ tables**, or any join onto a large/time-series table (records, positions,
  alerts, trips — TimescaleDB hypertables on Telemax2);
- `GROUP BY` / aggregates / window functions / `DISTINCT` over a large set;
- sub-queries, `EXISTS`/`ANY` over a collection, `Contains` with a list that is not small and bounded;
- recursive / hierarchical walks (company tree, parent chains);
- date-range scans, reports, exports, paging over a large table, or anything without a selective
  indexed predicate;
- raw SQL, `FromSqlRaw`, bulk `ExecuteUpdate` / `ExecuteDelete`;
- a query on a hot path (per message, per batch, per request on a high-traffic endpoint).

## The brainstorm — what to present before writing code

Present it to the user in the plan (or in chat) and **wait for a go-ahead**:

1. **The question in one line** — what rows, for whom (tenant scope: `CompanyId` + `IsDeleted`), how many
   expected (order of magnitude today and in a year).
2. **2–3 candidate shapes**, e.g. single projected query with joins vs. two queries + in-memory map vs.
   a pre-aggregated / cached source vs. a raw SQL / view.
3. **For each candidate**: round-trips, indexes it relies on (name them; say if one is missing), expected
   rows scanned vs. returned, memory pulled into the app, and lock/write impact if it writes.
4. **The generated SQL** of the favourite — EF Core: `query.ToQueryString()`; Prisma: query logging — and,
   when the table is large, the `EXPLAIN (ANALYZE, BUFFERS)` against a realistic DB (never run `ANALYZE`
   of a write on production).
5. **Recommendation + why**, and whether a new index / migration is needed (if so it follows the migration
   review — Telemax2: [`telemax2-knowledge/04`](../telemax2-knowledge/04-dataservice-db-impact-review.md)).

Do not start implementing the complex query until the user has confirmed the shape. If the chosen shape
changes mid-implementation, re-confirm — don't swap silently.

---

## ❌ Don't — first shape that compiled

```csharp
// "Alerts per vehicle for the last 30 days" — written straight away
var vehicles = await db.Vehicles.Where(v => v.CompanyId == companyId).ToListAsync(ct);
foreach (var v in vehicles)
{
    v.AlertCount = await db.AlertRecords                 // ← N+1 over a hypertable
        .CountAsync(a => a.VehicleId == v.Id && a.VehicleDate >= from, ct);
}
```

## ✅ Do — compare, confirm, then one set-based query

> **Option A** — one `GROUP BY VehicleId` on `AlertRecords` filtered by the company's vehicle ids + date
> range; 1 round-trip, uses `(VehicleId, VehicleDate)` index, returns ≤ N rows. **Option B** — read the
> daily pre-aggregate if one exists; cheaper but stale up to 1 day. **Recommend A** (needs to be live).
> → *user confirms A* → implement:

```csharp
var counts = await db.AlertRecords
    .Where(a => vehicleIds.Contains(a.VehicleId) && a.VehicleDate >= from)
    .GroupBy(a => a.VehicleId)
    .Select(g => new { VehicleId = g.Key, Count = g.Count() })
    .ToDictionaryAsync(x => x.VehicleId, x => x.Count, ct);   // one query, server-side aggregate
```

---

## Exceptions

- **Simple query** (none of the triggers above): write it directly — still no N+1.
- **The user already specified the query shape** in the ticket or chat: confirm you read it the same way in
  one line, then implement — no need to re-brainstorm alternatives.
- **Re-using an existing, proven query** unchanged (calling an existing service method): no brainstorm, but
  check it is not being called once per item.
