# A user assigned to a company sees that company's whole subtree

> **Applies to**: any `Telemax2` code that lists or filters companies for a user — the company
> switcher/dropdown, login/refresh company sets, `AccountService.GetCompaniesForUserAsync`,
> `CompanyService.GetActiveCompaniesForUserAsync`, `CompaniesToUsers`, visibility/suspension.

**Rule (MUST):** a user assigned to **any** company can see that company **and all of its descendant
companies (child, grandchild, … recursively)** — not only the companies they are directly assigned to.
Every endpoint that returns "companies for a user" MUST return the **same set** as the login path
(`AccountService.GetCompaniesForUserAsync`, which expands to sub-companies). A refresh/secondary endpoint
that returns less will overwrite the correct list with an incomplete one.

**Suspension is effective over the whole chain:** a company is inactive when **itself OR any ancestor**
is suspended. Hide the entire subtree of a suspended company. Never decide visibility from a company's
own `IsSuspended` flag alone.

**Why (the failure it prevents):** TLM-3165 — the switcher dropdown lost child companies because a
post-login refresh called a method that returned only **direct** assignments
(`CompaniesToUsers where UserId == userId`), silently dropping every child the user wasn't explicitly
assigned to. Two same-named methods in different services diverged; the incomplete one overwrote the good
list from login.

---

## ❌ Don't — direct assignments only

```csharp
return await _dbContext.CompaniesToUsers
    .Where(x => x.UserId == userId)
    .Select(x => new Company(x.Company.Id, x.Company.ParentId, x.Company.Name))
    .ToListAsync(ct);        // ← drops all child companies the user isn't directly assigned to
```

## ✅ Do — assigned roots + their descendants, minus effectively-suspended

```csharp
var rootIds = await _dbContext.CompaniesToUsers
    .Where(x => x.UserId == userId && !x.Company.IsDeleted)
    .Select(x => x.CompanyId).Distinct().ToListAsync(ct);

if (rootIds.Count == 0) return [];                       // no assignments → empty, never throw

// expand to the whole subtree (bounded per-level queries — see ai/shared-be N+1 rule),
// then drop anything suspended itself or by an ancestor
return await GetVisibleDescendantCompaniesAsync(rootIds, ct);
```

## Mandatory edge cases
- User with **no assignments** (or all soft-deleted) → return **empty**, never throw (was a 500/NRE).
- Always exclude `IsDeleted` companies.
- Guard **parent cycles** in bad data (visited set) when walking the tree.
