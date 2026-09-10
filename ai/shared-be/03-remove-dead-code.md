# Remove Dead Code Before You Finish (Shared Backend)

> **Applies to**: every change, before you call it done — .NET (EF Core / services), Next.js route
> handlers, TypeORM, plain mappers. Cross-stack backend rule, the backend counterpart to `ai/shared-fe/`.
> "It compiles" is not "it's used."

**Rule (MUST):** every symbol a change adds — an interface member, a property, a field, a parameter, a
method, a `using`/`import`, a config key — **MUST have a real consumer within the same change**. If
nothing reads it, it is dead: **delete it**, don't ship it "in case." Run a final pass over the diff whose
only job is to find and remove what you added but never wired up.

**Why (the failure it prevents):** dead code is a lie the next reader believes. An interface member with no
caller looks like a contract someone depends on, so they preserve it, implement it, and reason about it —
paying forever for a line that does nothing. It also hides real bugs: the member you *meant* to consume
sits unread, the feature silently half-works, and the compiler stays green because an unused public
surface is legal.

The most common variant on this codebase: **an interface gains a member that only concrete types actually
read.** If every read site is `((ConcreteType)x).Member`, the member does not belong on the interface — it
is dead there.

---

## ❌ Don't — add an interface member nothing reads through the interface

```csharp
public interface IAlertEmailV1Model
{
    string? AlertRuleName { get; }
    int?    AlertRuleId   { get; }   // ← added here…
}

// …but every read is via the concrete type, never the interface:
var id = message switch {
    AlertMessage a    => a.AlertRuleId,     // concrete
    ReminderMessage r => r.AlertRuleId,     // concrete
};
// → the interface member is dead. Nothing binds IAlertEmailV1Model.AlertRuleId.
```

## ✅ Do — put the member where it is actually consumed

```csharp
public interface IAlertEmailV1Model
{
    string? AlertRuleName { get; }        // stays: the layout binds it via the interface
    // AlertRuleId is NOT here — no interface-level consumer exists.
}

public abstract class AlertMessage : IAlertEmailV1Model
{
    public int? AlertRuleId { get; set; } // lives on the concrete types that read it
}
```

Rule of thumb: **an interface member must have at least one read through the interface** (`IFoo x; … x.Member`).
If the only readers cast to a concrete type first, the member belongs on the concrete type.

---

## Final pass — dead-code checklist

Before finishing, walk the diff and delete any of these that your change introduced:

- [ ] **Interface members** with no read through the interface (all reads cast to a concrete type first).
- [ ] **Properties / fields** that are assigned but never read (or read but never assigned).
- [ ] **Methods / functions** with no caller.
- [ ] **Parameters** the body never uses.
- [ ] **`using` / `import`** lines nothing in the file needs.
- [ ] **Config keys** added to `appsettings*.json` / `.env` that no code reads.
- [ ] **Commented-out code** you added "for later" — delete it; git remembers.
- [ ] **Enum values / constants** with no reference.

If a member is genuinely for a consumer landing in a **later** change, that later change adds it — not this
one. Do not pre-add surface. (Cross-references: [`02-mirror-source-property-names.md`](./02-mirror-source-property-names.md).)
