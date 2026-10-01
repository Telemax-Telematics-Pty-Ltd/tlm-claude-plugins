# Dashboard dates: convert to the user's timezone, show no zone label

> **Applies to**: the `Telemax2` Blazor dashboard client (`Telemax.Dashboard.Client`): every date/time a page,
> panel, modal or row renders, revamp or legacy. **Not** HTML emails or other server-rendered messages; see
> the exception below.

**Rule (MUST):** the dashboard renders every instant **converted to the user's timezone** (the one in their
user settings, exposed as `IUserContext.TimeZoneInfo`) and formatted with the user's date format. It shows
**no timezone label** next to the time: no "AEST", no "UTC", no "UTC+7".

- APIs return UTC. Convert once on the client, at render time, with the user's zone:
  `((DateTime?)utc).ToTimeZone(_userContext.TimeZoneInfo.Id)` (Revamp vehicle pages wrap this as
  `VehicleDetailLocalTime.ToLocal`).
- When the server groups or words dates (day headings, "that day", sentences), pass the user's
  `timeZoneId` to the endpoint and convert there. Never group by UTC days.
- Format with the user's `DateFormat` (and units) from the user context or the endpoint's display settings,
  never a hard-coded `dd/MM/yyyy`.

**Why (the failure it prevents):** TLM-3442 install record showed `Installed 10/01/2026 3:29 pm UTC` for a user
whose timezone was not UTC. The time had been converted correctly, but the label came from guessing an
abbreviation off `TimeZoneInfo.StandardName`. In Blazor WASM that name is often an offset ("+07") or an IANA ID,
so the guess fell back to "UTC" and the page claimed the wrong zone. The user already chose their timezone in
settings, so every time on the dashboard is in it by definition. A label adds nothing, and guessing it is
unreliable in the browser.

---

## ❌ Don't: a zone label on a dashboard time

```csharp
// Label guessed from the zone's name - "UTC" for many zones in WASM.
private string StripTitle =>
    $"Installed {Format(Local(record.InstalledUtc))} {Abbreviate(_userContext.TimeZoneInfo, record.InstalledUtc)}";

// Raw UTC rendered as if it were local.
<span>@record.InstalledUtc.ToString("dd/MM/yyyy h:mm tt")</span>
```

## ✅ Do: converted to the user's zone, formatted by their settings, no label

```csharp
private string StripTitle =>
    $"Installed {VehicleDetailScreenFormats.DateTime(Local(record.InstalledUtc), Settings)}";

private DateTime? Local(DateTime utc) => ((DateTime?)utc).ToLocal(_userContext.TimeZoneInfo.Id);
```

---

## Exception: HTML emails and other off-dashboard messages MUST show the zone label

Emails (and SMS, PDFs, anything read outside the dashboard) are opened without the user's settings in view,
are forwarded to people in other zones, and sit in an inbox long after they were sent. There the time **must
carry its zone label** ("5:31 pm AEST"). The backend preformats it, zone label included, before it reaches the
template ([`shared-fe/17` §6](../shared-fe/17-email-templates.md)).

These are two different rules. Don't copy the email's labelling logic into a dashboard page, and don't drop the
label from an email because the dashboard has none.
