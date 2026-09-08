# Avoid N+1 Queries (Shared Backend)

> **Applies to**: any server that talks to a database through an ORM or query builder — Prisma
> (Next.js route handlers / API), EF Core (.NET), TypeORM, Sequelize, raw SQL. Cross-stack backend rule,
> the backend counterpart to `ai/shared-fe/`.

**Rule:** never issue one query per item of a collection. Load the related data a collection needs in
**one** round-trip — via the ORM's `include`/`join`/projection, or a single batched `WHERE id IN (…)` —
not by re-querying inside a loop (or once per emitted item). Fall back to a per-item query **only** when
batching is genuinely impossible, and then bound and document it (see Exceptions).

**Why (the failure it prevents):** an N+1 is 1 query for the list + 1 more for each of its N items. It
looks fine with 5 rows in dev and melts the database at 5,000 in prod — latency and DB load grow linearly
with N, the connection pool starves, and the endpoint times out under exactly the load you shipped it
for. The worst variant re-queries data the request **already holds in memory**.

---

## ❌ Don't — a query per item

```csharp
// EF Core: one extra round-trip per reminder that gets dispatched
foreach (var reminder in dueReminders)
{
    var v = await db.Vehicles
        .Where(x => x.Id == reminder.VehicleId)
        .Select(x => new { x.NumberPlate, x.CreatedBy.Email })
        .FirstOrDefaultAsync(ct);          // ← N+1
    Send(reminder, v);
}
```

```ts
// Prisma: same shape
for (const order of orders) {
  const customer = await prisma.customer.findUnique({ where: { id: order.customerId } }); // ← N+1
}
```

## ✅ Do — one query that carries what you need

**1. Include/join the relation in the query that already loads the collection** (best — you own that query):

```csharp
var dueReminders = await db.Reminders
    .Where(/* … */)
    .Select(r => new { r.Id, r.VehicleId, Plate = r.Vehicle.NumberPlate, OwnerEmail = r.CreatedBy.Email })
    .ToListAsync(ct);        // rego + owner arrive WITH the list — zero extra round-trips
```

```ts
const orders = await prisma.order.findMany({ where: { /* … */ }, include: { customer: true } });
```

**2. Batch by id when you can't touch the first query** — collect ids, one `IN` query, map in memory:

```csharp
var ids = items.Select(i => i.VehicleId).ToHashSet();
var plates = await db.Vehicles
    .Where(v => ids.Contains(v.Id))
    .ToDictionaryAsync(v => v.Id, v => v.NumberPlate, ct);   // one query, not N
foreach (var i in items) Use(plates.GetValueOrDefault(i.VehicleId));
```

**3. If the data is already loaded, don't re-query it** — thread the in-memory value through (a DTO field,
a method parameter) instead of fetching it again in a downstream helper. Re-fetching what you already have
is an N+1 with no upside.

---

## Exceptions — "unless there is no other way"

A per-item call is acceptable only when batching is genuinely unavailable, and then you must **bound** and
**document** it:

- a third-party / cross-service call with **no batch endpoint** — cap concurrency, cache by key, and
  comment why it can't be batched;
- provider APIs that accept a selector — **chunk** (e.g. 100 ids/request), never 1/request, where allowed.

Any per-item query that survives review MUST carry a `// N+1 unavoidable: <reason>` comment, so the next
reader knows it was a deliberate decision, not an oversight. When in doubt, measure: an N+1 hides until the
collection grows.
