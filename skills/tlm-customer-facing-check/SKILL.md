---
name: "tlm-customer-facing-check"
description: "Use before sharing anything with a Telemax customer (spreadsheets, CSVs, docs, PDFs, decks, emails, screenshots, links): remove supplier and internal details, rewrite in plain English, flag anything unsure."
---

# Telemax customer-facing check

Run this over anything a Telemax team member is about to share with a customer: dev exports, data checks, reports, documents, decks, email drafts, screenshots and links. The customer version shows only that customer's data, in Telemax's own words, with nothing about how the platform is built, who builds it, or what it costs.

Keep the original unchanged and write the customer version as a new file.

Share with customers online only, as a link Telemax controls and can update (Google Sheets, Google Docs, Google Slides, or a page in the Telemax app). Send no downloadable copies: no .xlsx, .csv, .docx, .pdf or .pptx attachments. See section 8.

When something isn't covered here, or a rule needs an exception, flag it and tell the person to check with Steph or Ash before sending.

## 1. Ask first

Ask these unless the request already answers them:

1. **Who is the customer?** Everything in the file must belong to that customer only.
2. **Has the customer already received a version?** If yes, say plainly that the new file does not replace theirs, and that renamed sheets, headers or codes will be visible if they compare the two.
3. **Which mode?**
   - **Keep the look**: same layout as a version the customer has already seen. Keep sheets, columns, styling, formulas and filters as they are, change only the wording, and flag section 3 items instead of removing them.
   - **Clean rebuild**: remove everything in sections 2 and 3, rewrite in plain English and apply the Telemax brand.

## 2. Suppliers and platform names

Replace or remove:

- **flespi:** say "data feed". Remove flespi device types and IDs (e.g. "device type 171"), channel, calculator and stream IDs.
- **Compass IoT, Native Connect, "connected car":** say "OEM" as the telemetry source ("OEM data", "OEM telemetry"). Use "connected car" only where Steph or Ash confirm that customer already uses the term.
- **Suppliers and tools:** Mapbox, SendGrid, Twilio, Xero, Freshdesk, ClickUp, Azure, Azure DevOps, AWS, Blazor, TailAdmin, Figma, Canva, GitHub, Claude and other AI tools, hosting providers. Remove them or describe what the thing does ("email alerts", "map", "support desk").
- **Tollio, Tollify and DriveIQ:** remove every mention, in any context and any spelling, with no replacement name. They never appear in anything a customer sees.
- **Codes, sheet names and headers** that contain a supplier name: rename them (NOT_IN_FLESPI becomes NOT_IN_DATA_FEED) and update formulas that reference them.

These can stay:

- Teltonika and tracker model names (e.g. FMC003)
- Stripe, in billing and payment context only
- The OpenStreetMap credit on any map that uses it (legally required)

## 3. Internal details

Remove (in Keep the look mode, flag them instead):

- **Other customers:** rows, names, account names and config keys belonging to any other customer (e.g. Sixt). Filter data to the one customer.
- **Internal and test accounts:** "ZZZ" accounts (e.g. ZZZ KARMO), TEST ACCOUNT, demo accounts, holding companies such as "Compass Intake".
- **Internal system and code names:** Telemax2, service and project names (e.g. Telemax.CompassIoTService), Depot, Telemax-Ops, telemax-orders.
- **Environments:** stage, dev, UAT and test data, and the words prod, production, stage, dev, UAT.
- **Internal IDs:** company and branch IDs (show company names), record IDs (vehicle, connected-car, tracker vehicle) unless the customer uses them in Telemax.
- **Device identifiers:** IMEIs, SIM numbers, ICCIDs, unless the document is about the customer's devices.
- **Technical leftovers:** database table, column and enum names (DataProviderId, VinLookupProcessed, "Type 0"), SQL, error and log text, API keys and tokens, file paths, script and CSV file names.
- **Run notes:** "linked by this run", "excluded on request", "checked against", internal reasoning.
- **Words that point to internal problems:** "bug", "workaround", "manual fix", "orphaned", "hardcoded", "data provider". Describe the outcome for the customer instead.
- **Commercial details:** supplier costs, margins, other customers' pricing, and internal reasons behind decisions (e.g. "no Mapbox in reports because of cost").
- **People and location:** developer and PM names (e.g. Darius, Jim, Kelvin, Tony) can stay. Remove HB Labs (any spelling: HB Labs, HBLab, HBLAB, hblabs), its management staff (e.g. Mike), and where the developers are based (Vietnam, Hanoi). Refer to the team as "the developers" or "our team".

## 4. Hidden content by format

Check the places people don't see on screen:

- **Spreadsheets:** hidden sheets, rows and columns, comments and notes, named ranges, data validation lists, pivot caches, external links, cells outside the used area, file properties (author, last modified by, title).
- **CSV:** every column, including ones that look empty at the top.
- **Word and PDF:** tracked changes, comments, headers and footers, alt text, embedded files, bookmarks, file properties. For a PDF, rebuild it from a clean source rather than covering text with boxes.
- **Slides:** speaker notes, hidden slides, off-canvas objects, alt text, file properties.
- **Emails:** forwarded internal threads, internal CC and BCC, internal signatures, attachments (run each one through this skill).
- **Screenshots and images:** URLs and browser tabs, account selectors or lists showing other customers, admin menus, stage banners, developer tools, internal chat or tickets. Crop, or retake in the customer's own account.
- **Links:** remove links to internal tools (ClickUp, Figma, Azure DevOps, GitHub, Claude artifacts, admin, stage or dev URLs). Link only to the live app, the public site or a file shared with the customer.

## 5. Plain English

- Give each issue code a plain-English label and meaning the customer can act on. Say what Telemax is doing about it only where the person confirms it; otherwise flag it.
- Show colours as the closest plain colour (Grey, not Gunmetal).
- Describe Telemax data as "vehicle and telemetry data". Telemax has no driver data.
- Use commas in text and spacing between values. Leave out the middle dot and em dashes.
- Convert UTC timestamps to the customer's local time and label the time zone.

## 6. Brand (Clean rebuild)

Apply the telemax-brand skill: the official logo (blue on light backgrounds), Montserrat, brand colours and table styles.

## 7. Verify

- Search the whole file, including the hidden places in section 4, for every term in sections 2 and 3. Ignore matches inside VINs, plates or row numbers.
- Recalculate formulas and check totals match the original.
- Check the file properties show Telemax, not a person or tool.

## 8. Share online

- Put the customer version in Google Sheets, Docs or Slides (an .xlsx becomes a Google Sheet, a .docx a Google Doc, a .pptx Google Slides).
- Share with the customer's email addresses as **Viewer**, not "Anyone with the link".
- In the share settings, turn off download, print and copy for viewers.
- Make updates in the same file so the customer's link always shows the current version. Make a new file only for a new report.
- If the customer asks for a file to download, check with Steph or Ash before sending one.
- Tell the person that viewers can still take screenshots or retype the content, so the scrub in sections 2 to 4 still has to be complete.

## 9. Hand back

In dot points, list:

- the link and its share settings
- what changed
- anything flagged to check with Steph or Ash
- the note about the version the customer already has, if one was sent