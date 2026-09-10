# Mirror the Source Name on Carrier Properties (Shared Backend)

> **Applies to**: any DTO / message / view-model / API-response property that simply **carries** a value
> read straight from a source field (an entity column, an upstream record, another DTO). Cross-stack
> backend rule — EF Core (.NET), Prisma (Next.js API), TypeORM, plain mappers. The backend counterpart to
> `ai/shared-fe/`.

**Rule (MUST):** a carrier property **MUST NOT re-word** the name of the value it carries. When a property
passes a value through unchanged, name it after the **source field**, not a re-worded synonym. If the
source is `IsEngineStarted`, the carrier is `IsEngineStarted` — not `IsEngineOn`. If the source is
`EngineCoolantTemp`, the carrier is `EngineCoolantTemp` — not `EngineTemp`. Rename only when you genuinely
**transform** the value (aggregate, derive, change meaning); a straight pass-through keeps the source's name.

**And keep the sibling's stem.** When the type already exposes a related property for the same concept, a
new companion **MUST** keep that established stem, not drop it. A message that already has `AlertRuleName`
gets `AlertRuleId` for the rule's id — **never** a stem-dropped `RuleId`. Half-renamed siblings
(`AlertRuleName` beside `RuleId`) read as two different things and break `grep AlertRule`.

**Why (the failure it prevents):** a re-worded pass-through desyncs two names for one value. Three costs:

1. **Traceability dies.** `grep IsEngineStarted` no longer finds the property that carries it, so the next
   reader can't follow the value from source to email/response without reading the mapper line by line.
2. **It invites a meaning flip.** `IsEngineOn` reads as the negation-prone twin of `IsEngineStarted`; the
   day someone wires `IsEngineOn = !record.IsEngineStarted` "to make the name true," the bug looks correct.
   Identical names make the mapping self-checking — `X = source.X` is obviously right.
3. **It fragments the vocabulary.** One codebase ends up with `EngineTemp`, `EngineTemperature` and
   `EngineCoolantTemp` for the same reading, and no one can tell if they mean the same thing.

---

## ❌ Don't — re-word a pass-through

```csharp
// The property invents a new name for a value it copies verbatim.
new LowBatteryVoltageAlertMessage {
    IsEngineOn = record.VehicleRecord?.IsEngineStarted,      // ← name ≠ source; reads as its own negation
    EngineTemp = record.VehicleRecord?.EngineCoolantTemp,    // ← abbreviated + drops "Coolant"
};
```

```ts
// Prisma → DTO: same shape
return { engineOn: row.isEngineStarted, temp: row.engineCoolantTemp }; // ← two renames, zero transforms
```

## ✅ Do — keep the source's name

```csharp
new LowBatteryVoltageAlertMessage {
    IsEngineStarted   = record.VehicleRecord?.IsEngineStarted,     // X = source.X — self-checking
    EngineCoolantTemp = record.VehicleRecord?.EngineCoolantTemp,
};
```

```ts
return { isEngineStarted: row.isEngineStarted, engineCoolantTemp: row.engineCoolantTemp };
```

### Sibling stem — the id companion of a named property

```csharp
// ❌ The message already exposes AlertRuleName; a stem-dropped id companion desyncs the pair.
public string? AlertRuleName { get; set; }
public int?    RuleId        { get; set; }        // ← drops "AlertRule"; grep AlertRule misses it
result.RuleId = snapshot.Alert.Id;

// ✅ Keep the sibling's stem.
public string? AlertRuleName { get; set; }
public int?    AlertRuleId   { get; set; }        // sibling of AlertRuleName — one vocabulary, grep-able
result.AlertRuleId = snapshot.Alert.Id;
```

---

## Exceptions — when a different name is correct

- **You actually transform the value** — an aggregate, a computed/derived field, a unit conversion, a
  join of several sources. Then the name describes the *result*, not any one input (e.g.
  `AverageSpeedKmh`, `TotalTripDistanceKm`).
- **A unit/type suffix for clarity** is fine **as long as the stem is preserved and consistent** within
  the type — `TotalDistance` → `TotalDistanceKm` keeps the stem; `EngineCoolantTemp` → `EngineTemp` does
  not (it drops a word). Pick one suffix convention per message and hold it.
- **A deliberate abstraction** across genuinely differently-named sources (the DTO is the seam between two
  vocabularies). Then it is a decision, not a slip — add a one-line comment saying which sources it
  unifies and why, so the next reader knows the mismatch is intentional.

When none of these apply, the property is a pass-through: give it the source's name.
