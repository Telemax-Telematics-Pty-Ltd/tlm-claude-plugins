# Dashboard FE naming — one feature prefix, pages end in `Page`

> **Applies to**: the `Telemax2` Blazor dashboard client (`Telemax.Dashboard.Client`) — every new or reworked
> screen folder under `Components/**/Views/` (revamp or legacy), its modals, its code-behind helpers and its
> story-book wrappers.

**Rule (MUST):** every component and helper that belongs to one screen family carries **the same feature
prefix**, named after the screen the user sees (e.g. `VehicleDetail`) — not after the data model (`Record`),
not after the version (`V3`), and not a generic word (`Screen`, `Flow`). Routed pages are the only files whose
name ends in `Page`, and the only files with an `@page` directive.

| What | Pattern | Example (Vehicle Details, TLM-3442) |
|---|---|---|
| Main routed page | `{Feature}Page.razor` | `VehicleDetailPage.razor` → `/manage/vehicles-v3/{id}` |
| Other routed pages of the family | `{Feature}{Screen}Page.razor` | `VehicleDetailInstallRecordPage.razor`, `VehicleDetailEngineCodePage.razor` |
| Child component (not routed) | `{Feature}{Part}.razor` — never ends in `Page` | `VehicleDetailHero`, `VehicleDetailActivityRow`, `VehicleDetailInstallPhotos` |
| Modal / dialog | `{Feature}{Name}Modal.razor` | `VehicleDetailPlateModal`, `VehicleDetailRemoveModal` |
| Non-component helper | `{Feature}{Role}.cs` | `VehicleDetailRoutes`, `VehicleDetailFormats` |
| Story-book wrapper | `{Feature}{Screen}ScenarioPage.razor` | `VehicleDetailInstallRecordScenarioPage` |

- The `.razor.cs` / `.razor.scss` files take the component's name, so they follow automatically.
- The **folder and the route may keep the version** (`Views/VehicleV3/`, `/manage/vehicles-v3/…`): the version
  is where the screen lives, the prefix is what it is. Renaming a route is a product change; renaming a type is not.
- Shared DTOs / enums in `Telemax.Dashboard.Shared` keep their contract names (`VehicleV3RecordItem`,
  `RecordMenuAction`) — this rule is about client components, not API contracts.
- Truly cross-feature components (review aids like `MockMarker`, design-system components in
  `Components/Revamp/Ui/`) take no feature prefix.

**Finding the entry point:** a view's entry point is the `.razor` file with `@page`. With the rule above it is
also the file ending in `Page`, so either works:

```bash
grep -l "@page" Telemax.Dashboard.Client/Components/Revamp/Views/VehicleV3/*.razor
```

**Why (the failure it prevents):** TLM-3442 — the Vehicle V3 folder held 30 `.razor` files. Parts were
`Record*` (`RecordPage`, `RecordHero`, `RecordRail`…), sub-screens were un-prefixed (`InstallRecordPage`,
`EngineCodePage`, `InstallPhotos`), modals were generic (`PlateModal`, `FlowField`). The reviewer could not
tell which file was the screen and which were its parts, nor which screen a part belonged to. Because Blazor
derives the BEM block class from the type name (`@Bem()` → `vehicle-detail-hero__…`), a generic name also
risks two features emitting the same block name.

---

## ❌ Don't — mixed prefixes, data-model names, `Page` ambiguity

```
Views/VehicleV3/
  RecordPage.razor          ← routed, but "Record" says nothing about the screen
  RecordHero.razor          ← part of the same screen, same prefix as the page
  InstallRecordPage.razor   ← routed sub-screen, different (no) prefix
  InstallPhotos.razor       ← part of InstallRecordPage? of something else?
  Modals/PlateModal.razor   ← whose modal?
  ScreenFormats.cs          ← generic helper name
```

## ✅ Do — one prefix, `Page` only on routed files

```
Views/VehicleV3/
  VehicleDetailPage.razor                 @page "/manage/vehicles-v3/{Id:int}"
  VehicleDetailInstallRecordPage.razor    @page "/manage/vehicles-v3/{Id:int}/install-record"
  VehicleDetailEngineCodePage.razor       @page "/manage/vehicles-v3/{Id:int}/engine-codes/{Code}"
  VehicleDetailHero.razor
  VehicleDetailInstallPhotos.razor
  VehicleDetailRoutes.cs
  Modals/VehicleDetailPlateModal.razor
```

## When renaming an existing feature

- `git mv` each file (keeps history), then replace the identifiers with a **whole-word** match so contract types
  that merely start with the old word (`RecordBannerKind`, `RecordMenuAction`) are untouched.
- Grep for the old kebab block names (`record-hero__`, `record-page__`) in `*.ts`, Playwright specs and any
  `.scss` that targets another component's block — those are strings and do not rename with the type.
- `dotnet build` **and** `npm run build` (SCSS is compiled by webpack, not by the .NET build).
