# Telemax Design System — the visual source of truth

> **Every task that produces or changes UI follows this file.** Colors, type, spacing, radii,
> shadows, motion, icons and copy tone are decided here — not per screen, not per developer, and
> not by eyeballing a screenshot.

## 0. Where it comes from, and what wins

| | |
|---|---|
| **Canonical source** | Claude Design project **"Telemax Design System"** — `claude.ai/design/p/382db012-aad4-4de4-83b8-9b6fccfe790e` |
| **Owner** | Design. The plugin mirrors it; it does not fork it. |
| **Machine-readable token list** | `_adherence.oxlintrc.json` → `x-omelette.tokens` in that project |
| **Token stylesheet** | `colors_and_type.css` in that project |
| **Reference UI kit** | `ui_kits/dashboard/` in that project (TopNav, Button, StatusPill, Tabs, KpiCard, HealthBar, DataTable, FAB) |

**Authority order when two sources disagree** — highest wins:

1. **A Figma frame for THIS screen** (`tlm-figma-to-code` STEP 0). A real design beats a default.
   But a Figma *value* that has no token still gets mapped — see §5 Rule 2.
2. **This file / the Claude Design project.** The house default for every screen with no Figma.
3. **An explicit rule in the consuming project** (`CLAUDE.md`, `.cursorrules`, its own token file).
   A project that already ships a different palette is not retro-fitted silently — surface the
   conflict and ask (`tlm-project-setup` records it in `.claude/codebase-map.md`).
4. **A sibling repo's shipped UI** (`tlm-fe-coding` STEP 1.5) — for information order and labels,
   never for raw color/size values.

**Why the order matters.** The failure this prevents is real and expensive: a dashboard screen built
from a screenshot ships `#0077FF`, `#0076FE` and `#0075FF` across three cards. Nobody notices in
review; a rebrand then becomes a repo-wide hex sweep instead of a one-line token edit.

## 1. What Telemax looks like — the five things that define it

If you remember nothing else, remember these. They are what makes a screen "look Telemax", and what
a reviewer notices first when they are missing:

1. **One hero color: cobalt `#0075FF`.** Top nav, primary CTAs, active pagination, links, logo.
   It is an identity, not a general-purpose accent — do not use it to "make something pop".
2. **Warm off-white canvas `#F7F7F5`.** Not `#F9FAFB`, not pure gray. The warmth is deliberate: it
   softens a data-dense UI and lets the blue read as brand. Getting this wrong makes the whole app
   look like a generic admin template.
3. **Traffic-light semantics do the work.** Red `#F04438` / orange `#F79009` / green `#12B76A`,
   each with a 50-level tint for pill backgrounds. Status is color + glyph, never color alone.
4. **Soft rounded cards.** White fill, **no border**, 12px radius, soft `shadow-sm`, 20-24px padding.
   Cards prefer shadow over border — a bordered card is a tell that the system was not followed.
5. **The health gradient.** Red → orange → yellow → green, labelled `Critical ← → Optimal`. It is
   the signature pattern and the **only gradient in the system**.

## 2. Tokens — the complete set

These values are verbatim from `colors_and_type.css`. **Do not retype them into a component.**

### 2.1 Brand

| Token | Value | Use |
|---|---|---|
| `--tm-blue-50` | `#EAF4FF` | soft primary tint, info pill bg |
| `--tm-blue-100` | `#BFDCFF` | |
| `--tm-blue-200` | `#7FBAFF` | |
| `--tm-blue-300` | `#60A9FF` | |
| `--tm-blue-400` | `#2E8FFF` | |
| `--tm-blue-500` | `#0075FF` | **Primary** — logo, navbar, CTAs |
| `--tm-blue-600` | `#005FD1` | primary hover |
| `--tm-blue-700` | `#004AA3` | primary pressed |
| `--tm-primary` | = `blue-500` | |
| `--tm-primary-hover` | = `blue-600` | |
| `--tm-primary-press` | = `blue-700` | |
| `--tm-primary-soft` | = `blue-50` | |

### 2.2 Neutrals

| Token | Value | Use |
|---|---|---|
| `--tm-white` | `#FFFFFF` | card fill |
| `--tm-bg` | `#F7F7F5` | **app background** (warm off-white) |
| `--tm-bg-alt` | `#FAFAFA` | table row hover, secondary button hover |
| `--tm-border` | `#E4E7EC` | default border |
| `--tm-border-strong` | `#D0D5DD` | input / secondary-button outline, empty star |
| `--tm-divider` | `#EAECF0` | table row dividers, progress track |
| `--tm-text-1` | `#101828` | headings, primary text |
| `--tm-text-2` | `#344054` | body / cell text |
| `--tm-text-3` | `#4D5869` | secondary |
| `--tm-text-4` | `#667085` | tertiary / captions |
| `--tm-text-5` | `#98A2B3` | disabled / placeholder |
| `--tm-text-6` | `#BCC0C9` | table label gray |

### 2.3 Semantic (status)

| Token | Value | | Token | Value |
|---|---|---|---|---|
| `--tm-critical-500` | `#F04438` | | `--tm-success-500` | `#12B76A` |
| `--tm-critical-100` | `#FEE4E2` | | `--tm-success-300` | `#6BD2A2` |
| `--tm-critical-50` | `#FEF3F2` | | `--tm-success-100` | `#D1FADF` |
| `--tm-warning-500` | `#F79009` | | `--tm-success-50` | `#ECFDF3` |
| `--tm-warning-100` | `#FEF0C7` | | `--tm-info-500` | `#0075FF` |
| `--tm-warning-50` | `#FFFAEB` | | `--tm-info-50` | `#EAF4FF` |

**Health-score gradient stops** (in order — this is the canonical ramp):

`--tm-health-critical` `#F04438` → `--tm-health-warn` `#F79009` → `--tm-health-ok` `#FFD748`
→ `--tm-health-good` `#84E1BC` → `--tm-health-optimal` `#12B76A`

### 2.4 Type

Fonts: **Montserrat** (sans + display), **JetBrains Mono** (IMEIs, voltages, any monospace data).
No third font. Weights in use: 400 / 500 / 600 / 700 / **800** / 900.

| Token | `weight size/line-height` | Use |
|---|---|---|
| `--tm-display-1` | `800 44px/1.1` | hero numerals / marketing |
| `--tm-display-2` | `800 36px/1.15` | |
| `--tm-h1` | `800 28px/1.2` | page title (`letter-spacing: -0.01em`) |
| `--tm-h2` | `800 22px/1.25` | section title — "Fleet Pulse" (`-0.005em`) |
| `--tm-h3` | `700 18px/1.3` | card title |
| `--tm-kpi` | `800 32px/1.1` | **KPI numerals** |
| `--tm-kpi-lg` | `800 40px/1.05` | hero KPI |
| `--tm-body` | `500 14px/1.5` | default body |
| `--tm-body-strong` | `700 14px/1.5` | |
| `--tm-body-lg` | `500 16px/1.5` | |
| `--tm-label` | `600 13px/1.4` | form labels, column headers |
| `--tm-caption` | `500 12px/1.4` | captions, status pill text |
| `--tm-micro` | `600 11px/1.3` | tab count badges |
| `--tm-nav` | `700 15px/1` | top-nav items |
| `--tm-mono` | `500 13px/1.4` | JetBrains Mono |

**KPI numerals are always weight 800.** The bold numeral is the loudest thing on every screen — that
hierarchy is the product, not a preference.

### 2.5 Spacing — 4px base grid

`4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64` (`--tm-s-1` … `--tm-s-16`).

Card padding 20-24px, page gutters 24-32px, vertical section rhythm 24-32px.

> **The scale is already Tailwind's.** Tailwind's `--spacing` multiplier is `0.25rem` = 4px, so
> `--tm-s-6` (24px) **is** `p-6`, `--tm-s-10` (40px) **is** `p-10`, all the way through. No custom
> spacing tokens are needed on web — just never write `p-[22px]`.

### 2.6 Radii — rounded is a core brand feel

| Token | Value | Use |
|---|---|---|
| `--tm-r-sm` | `6px` | small chips |
| `--tm-r-md` | `10px` | **inputs, buttons, tabs, selects** |
| `--tm-r-lg` | `12px` | **cards**, tab containers |
| `--tm-r-xl` | `16px` | large panels |
| `--tm-r-pill` | `999px` | status pills, FAB, progress bars |

Nothing in Telemax is square. A `rounded-none` / `border-radius: 0` surface is a bug.

### 2.7 Shadows — soft and diffuse, never harsh

| Token | Value | Use |
|---|---|---|
| `--tm-shadow-xs` | `0 1px 2px rgba(16,24,40,0.05)` | inputs, buttons at rest, pressed state |
| `--tm-shadow-sm` | `0 1px 3px rgba(16,24,40,0.06), 0 1px 2px rgba(16,24,40,0.04)` | **cards** |
| `--tm-shadow-md` | `0 4px 8px -2px rgba(16,24,40,0.06), 0 2px 4px -2px rgba(16,24,40,0.04)` | hovered cards, dropdowns |
| `--tm-shadow-lg` | `0 12px 24px -4px rgba(16,24,40,0.08), 0 4px 8px -2px rgba(16,24,40,0.04)` | modals |
| `--tm-shadow-focus` | `0 0 0 4px rgba(0,117,255,0.20)` | **focus ring** |

**No inner shadows anywhere.**

### 2.8 Motion

| Token | Value |
|---|---|
| `--tm-ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` |
| `--tm-ease-std` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| `--tm-dur-fast` | `120ms` — hover transitions |
| `--tm-dur-base` | `180ms` — card lifts |
| `--tm-dur-slow` | `280ms` |

No bounces, no springs, no scale-to-grow, no page transitions. Data refreshes fade; filter chips
slide 2-4px. The FAB and AI buttons may carry a subtle pulsing glow — never a bounce.

## 3. Installing the tokens — web (Tailwind v4)

Copy `colors_and_type.css` from the design project into the repo **verbatim** as
`src/styles/telemax-tokens.css` and **never hand-edit it** — it is a mirror, and a new value comes
from re-copying it. Then bridge it into Tailwind so every token becomes a utility class:

```css
/* src/styles/globals.css */
@import "tailwindcss";
@import "./telemax-tokens.css";   /* mirror of the design system — do not edit */

/* `inline` is REQUIRED here: these reference other CSS variables, and without it a
   utility resolves --tm-* where the theme var is defined, not where it is used. */
@theme inline {
  /* --- color ------------------------------------------------------------- */
  --color-primary:        var(--tm-primary);
  --color-primary-hover:  var(--tm-primary-hover);
  --color-primary-press:  var(--tm-primary-press);
  --color-primary-soft:   var(--tm-primary-soft);

  --color-bg:             var(--tm-bg);
  --color-bg-alt:         var(--tm-bg-alt);
  --color-surface:        var(--tm-white);
  --color-border:         var(--tm-border);
  --color-border-strong:  var(--tm-border-strong);
  --color-divider:        var(--tm-divider);

  --color-text-1:         var(--tm-text-1);
  --color-text-2:         var(--tm-text-2);
  --color-text-3:         var(--tm-text-3);
  --color-text-4:         var(--tm-text-4);
  --color-text-5:         var(--tm-text-5);
  --color-text-6:         var(--tm-text-6);

  --color-critical:       var(--tm-critical-500);
  --color-critical-100:   var(--tm-critical-100);
  --color-critical-50:    var(--tm-critical-50);
  --color-warning:        var(--tm-warning-500);
  --color-warning-100:    var(--tm-warning-100);
  --color-warning-50:     var(--tm-warning-50);
  --color-success:        var(--tm-success-500);
  --color-success-100:    var(--tm-success-100);
  --color-success-50:     var(--tm-success-50);
  --color-info:           var(--tm-info-500);
  --color-info-50:        var(--tm-info-50);

  /* --- type: size + leading + weight travel together as ONE class --------- */
  --font-sans: var(--tm-font-sans);
  --font-mono: var(--tm-font-mono);

  --text-h1: 28px;        --text-h1--line-height: 1.2;      --text-h1--font-weight: 800;
  --text-h2: 22px;        --text-h2--line-height: 1.25;     --text-h2--font-weight: 800;
  --text-h3: 18px;        --text-h3--line-height: 1.3;      --text-h3--font-weight: 700;
  --text-kpi: 32px;       --text-kpi--line-height: 1.1;     --text-kpi--font-weight: 800;
  --text-kpi-lg: 40px;    --text-kpi-lg--line-height: 1.05; --text-kpi-lg--font-weight: 800;
  --text-body: 14px;      --text-body--line-height: 1.5;    --text-body--font-weight: 500;
  --text-label: 13px;     --text-label--line-height: 1.4;   --text-label--font-weight: 600;
  --text-caption: 12px;   --text-caption--line-height: 1.4; --text-caption--font-weight: 500;
  --text-micro: 11px;     --text-micro--line-height: 1.3;   --text-micro--font-weight: 600;
  --text-nav: 15px;       --text-nav--line-height: 1;       --text-nav--font-weight: 700;

  /* --- radius / shadow / ease -------------------------------------------- */
  --radius-sm:   var(--tm-r-sm);
  --radius-md:   var(--tm-r-md);
  --radius-lg:   var(--tm-r-lg);
  --radius-xl:   var(--tm-r-xl);
  --radius-pill: var(--tm-r-pill);

  --shadow-xs:    var(--tm-shadow-xs);
  --shadow-sm:    var(--tm-shadow-sm);
  --shadow-md:    var(--tm-shadow-md);
  --shadow-lg:    var(--tm-shadow-lg);
  --shadow-focus: var(--tm-shadow-focus);

  --ease-out-tm: var(--tm-ease-out);
  --ease-std:    var(--tm-ease-std);
}
```

This **deliberately remaps** Tailwind's stock `rounded-md` / `rounded-lg` / `shadow-sm` to Telemax
values (the "remap a stock scale" approach already endorsed in `02-styling-ui-conventions.md` §3), so
existing components inherit the system without a class sweep.

You then write `bg-primary`, `text-text-1`, `text-h2`, `rounded-lg`, `shadow-sm`, `border-border`.

**Durations have no `@theme` namespace in Tailwind v4.** Use the CSS variable directly:
`duration-[var(--tm-dur-fast)]` (valid on v3 and v4) or the v4 shorthand `duration-(--tm-dur-fast)`.

### Tailwind v3 projects

Same idea in `tailwind.config.ts` → `theme.extend`: `colors`, `fontSize` (tuple form
`['22px', { lineHeight: '1.25', fontWeight: '800' }]`), `borderRadius`, `boxShadow`. The `--tm-*`
mirror file still ships and is still the source; the config reads from it via `var()`.

## 4. Installing the tokens — React Native

There is no CSS. The mirror becomes a **typed theme constants module**, and it is the only file in
the app allowed to contain a literal color or size:

```ts
// src/_modules/config/theme.ts — mirror of the Telemax Design System. Do not invent values here.
export const colors = {
  primary: '#0075FF',
  primaryHover: '#005FD1',
  primaryPress: '#004AA3',
  primarySoft: '#EAF4FF',
  bg: '#F7F7F5',
  bgAlt: '#FAFAFA',
  surface: '#FFFFFF',
  border: '#E4E7EC',
  borderStrong: '#D0D5DD',
  divider: '#EAECF0',
  text1: '#101828',
  text2: '#344054',
  text3: '#4D5869',
  text4: '#667085',
  text5: '#98A2B3',
  text6: '#BCC0C9',
  critical: '#F04438',
  critical50: '#FEF3F2',
  warning: '#F79009',
  warning50: '#FFFAEB',
  success: '#12B76A',
  success50: '#ECFDF3',
} as const;

export const healthRamp = ['#F04438', '#F79009', '#FFD748', '#84E1BC', '#12B76A'] as const;

export const radii = { sm: 6, md: 10, lg: 12, xl: 16, pill: 999 } as const;
export const spacing = { s1: 4, s2: 8, s3: 12, s4: 16, s5: 20, s6: 24, s8: 32, s10: 40, s12: 48, s16: 64 } as const;
export const durations = { fast: 120, base: 180, slow: 280 } as const;

export const typography = {
  h1:      { fontFamily: 'Montserrat_800ExtraBold', fontSize: 28, lineHeight: 34 },
  h2:      { fontFamily: 'Montserrat_800ExtraBold', fontSize: 22, lineHeight: 28 },
  h3:      { fontFamily: 'Montserrat_700Bold',      fontSize: 18, lineHeight: 23 },
  kpi:     { fontFamily: 'Montserrat_800ExtraBold', fontSize: 32, lineHeight: 35 },
  body:    { fontFamily: 'Montserrat_500Medium',    fontSize: 14, lineHeight: 21 },
  label:   { fontFamily: 'Montserrat_600SemiBold',  fontSize: 13, lineHeight: 18 },
  caption: { fontFamily: 'Montserrat_500Medium',    fontSize: 12, lineHeight: 17 },
  mono:    { fontFamily: 'JetBrainsMono_500Medium', fontSize: 13, lineHeight: 18 },
} as const;
```

RN specifics that differ from web:

- `fontWeight` is **not reliable** with custom fonts — load the named weight family
  (`Montserrat_800ExtraBold`) via `expo-font` / `@expo-google-fonts/montserrat` and set `fontFamily`.
  Setting `fontWeight: '800'` on top of a 500-weight family gets you a synthesized bold on iOS and
  is ignored on Android.
- Wrap sizes in the project's `scale()` helper as usual (`ai/reactnative/02-styling-stylesheet.md`);
  the numbers above are the 1x design values.
- `shadow-*` does not port — use `elevation` on Android plus `shadowColor: '#101828'` with the
  matching opacity/radius on iOS, exposed as shared `shadowSm` / `shadowMd` style objects in this file.
- There is no `999px` pill trick on a variable-height view; use `borderRadius: height / 2` or a
  large constant on a fixed-height element.

## 5. HARD RULES

### Rule 1 — No raw color, size, radius, shadow or font value in a component. Ever.

A component names a token. Values live in exactly one file per platform (§3 / §4).

```tsx
// ❌ every one of these is a violation
<Col className="bg-[#0075FF] rounded-[12px] p-[22px] shadow-[0_1px_3px_rgba(0,0,0,0.06)]">
<TextPrimary style={{ color: '#101828', fontSize: 22 }}>
<Col className="bg-blue-500">                 {/* stock Tailwind palette is NOT Telemax blue */}

// ✅
<Col className="bg-primary rounded-lg p-6 shadow-sm">
<TextPrimary className="text-h2 text-text-1">
```

**Why.** `#0075FF` typed by hand appears as `#0077FF` within a sprint, and a rebrand becomes a
repo-wide sweep instead of one line. It also breaks the adherence lint in the design project.

**Exempt files only:** the token mirror (`telemax-tokens.css` / `config/theme.ts`), the Tailwind
config, and SVG/logo assets. Nothing else — not "just this one chart color".

### Rule 2 — A Figma value with no token gets mapped, and the mismatch is reported.

Figma wins on *layout and content*. It does **not** license a new hex. When a Figma frame hands you
`#0074FE`, a `13px` radius or a 15px body size:

1. Snap it to the nearest token (`--tm-primary`, `--tm-r-lg`, `--text-body`).
2. **Say so in the summary**, one line per mapping: `Figma #0074FE → --tm-primary (#0075FF)`.
3. If it is genuinely a new value the system needs (a new status color, a new chart series),
   **stop and ask** — it is a token addition owned by design, not a component decision.

**Why.** Figma frames drift from the system all the time (a copy-pasted layer, an old file). Silently
honouring the drift is how a design system dies one screen at a time.

### Rule 3 — The app background is `#F7F7F5`, cards are white with no border.

```tsx
// ❌ generic-admin look: cool gray page, bordered card
<Col className="bg-gray-50 min-h-screen">
  <Col className="bg-white border border-gray-200 rounded-lg p-4">

// ✅
<Col className="bg-bg min-h-screen">
  <Col className="bg-surface rounded-lg shadow-sm p-6">
```

A card gets **shadow, not border**. Borders are for inputs, tabs and table dividers.

### Rule 4 — Status is color **and** glyph, from the semantic set.

A status pill is `rounded-pill`, 50-level background, 500-level text, 12px/700, with a leading SVG
icon and 4px gap:

```tsx
// ✅ tone drives BOTH the tint and the glyph
<Row className="items-center gap-1 rounded-pill bg-success-50 px-2.5 py-1">
  <IconCheckCircle className="size-4 text-success" />
  <TextPrimary className="text-caption font-bold text-success">{t('battery.optimal')}</TextPrimary>
</Row>
```

```tsx
// ❌ color-only status — invisible to a red/green colorblind user and in grayscale print
<TextPrimary className="text-success">{t('battery.optimal')}</TextPrimary>
```

Tones: `success` / `warning` / `critical` / `info` (`#EAF4FF` bg + `#004AA3` text) /
`neutral` (`#F2F4F7` bg + `--tm-text-2`). Map them with a `Record<EStatusTone, …>`, never a ternary
chain (`04-typescript-enums-constants.md`).

### Rule 5 — The health gradient is the only gradient, and it is always labelled.

Score bars use the five-stop ramp and carry the `Critical ← → Optimal` end labels. Any other
gradient — a gradient button, a gradient card header, a gradient nav — is outside the system.

```tsx
// ✅ track + gradient fill + end labels
<Col className="gap-1">
  <Col className="h-2 w-full overflow-hidden rounded-pill bg-divider">
    <Col
      className="h-full rounded-pill bg-[linear-gradient(90deg,var(--tm-health-critical),var(--tm-health-warn),var(--tm-health-ok),var(--tm-health-good),var(--tm-health-optimal))]"
      style={{ width: `${score}%` }}
    />
  </Col>
  <Row className="justify-between">
    <TextPrimary className="text-micro text-text-4">{t('score.critical')}</TextPrimary>
    <TextPrimary className="text-micro text-text-4">{t('score.optimal')}</TextPrimary>
  </Row>
</Col>
```

The `linear-gradient(...)` composed from `var(--tm-health-*)` is token-backed and therefore allowed —
it is the one place a `bg-[...]` arbitrary value is correct. A percentage `width` from live data is a
runtime value, not a design token, so the inline `style` is correct here too.

### Rule 6 — Focus rings are never removed.

`outline-none` without a replacement ring is a hard violation. Every interactive element gets
`focus-visible:shadow-focus` (the 4px `rgba(0,117,255,0.20)` ring) plus a 1px primary edge. This
compounds with the affordance pass in `12-interactive-affordances.md` — pointer cursor, hover state,
24px hit target — which still applies in full.

### Rule 7 — No emoji, no Unicode pictographs, no icon font.

Icons are **Lucide** SVGs (see §7). A star, warning triangle, check mark or any emoji character
never appears in UI copy or as a status glyph — they render differently on every OS and cannot take
a `stroke-width`. This is a content rule as much as a visual one, and it applies to toast messages,
empty states and table cells too.

### Rule 8 — Montserrat and JetBrains Mono. No third font.

Body/display is Montserrat; IMEIs, voltages, coordinates and other fixed-width data are JetBrains
Mono. Any other `font-family` is a violation — including a system-stack fallback introduced by
copy-pasted markup.

## 6. Component specs

Exact values from the reference UI kit. Build these as `Base*` primitives once; screens consume them.

### Button

| | Primary | Secondary | Ghost | Danger |
|---|---|---|---|---|
| background | `--tm-primary` | `#FFFFFF` | transparent | `--tm-critical-500` |
| text | `#FFFFFF` | `--tm-text-2` | `--tm-primary` | `#FFFFFF` |
| border | none | `1px --tm-border-strong` | none | none |
| shadow | `--tm-shadow-xs` | `--tm-shadow-xs` | none | `--tm-shadow-xs` |
| hover | `--tm-primary-hover` | bg `#FAFAFA` | bg primary @ 8% | `#D92D20` |

Shared: `font-weight 700`, radius **10px** (`rounded-md`), `display: inline-flex`, `gap: 8px`,
`white-space: nowrap`, `cursor: pointer`, transition `120ms cubic-bezier(0.4, 0, 0.2, 1)`.
Sizes: **md** `14px / 10px 16px`, **sm** `13px / 7px 12px`. Leading icon 16px, stroke 2.

Pressed: background `--tm-primary-press`, shadow collapses to `xs`. **No scale transform.**

### Status pill
`radius 999px`, padding `4px 10px`, `12px/700`, `gap 4px`, 50-level bg + 500-level text.

### Tabs
Container: white, `padding 4px`, `radius 10px`, `box-shadow: inset 0 0 0 1px --tm-border`.
Item: `padding 8px 14px`, `radius 8px`, `13px/600`. Active → `color --tm-text-1`, `bg #F2F4F7`,
`shadow 0 1px 2px rgba(16,24,40,0.06)`. Inactive → `color --tm-text-4`, transparent.
Count badge: `radius 999px`, `padding 1px 7px`, `11px/700`; active = primary bg + white text,
inactive = `--tm-divider` bg + `--tm-text-2`.

### SegmentedControl
`border 1px --tm-border-strong`, `radius 10px`, `overflow: hidden`; segment `padding 7px 14px`,
`13px/600`; selected = primary bg + white text; 1px divider between segments.

### Select / SearchField
White, `border 1px --tm-border-strong`, `radius 10px`. Select `padding 8px 12px`, `13px/600`, trailing
chevron. SearchField `padding 9px 14px`, `min-width 260px`, leading search icon, `14px` input text in
`--tm-text-1`; the inner input carries no border or outline of its own.

### Card / KPI card
White, **no border**, `radius 12px`, `shadow-sm`, padding 20-24px.
KPI cards follow a fixed vertical rhythm, in this order:
**small label (`--tm-label`, `--tm-text-4`) → large numeral (`--tm-kpi`, weight 800, `--tm-text-1`) →
sub-unit / delta → thin progress or gradient bar.** Do not reorder it per card.

### Table
Row divider `1px --tm-divider` — never heavier. Column header `--tm-label`. Row hover `#FAFAFA`.
Cell text `--tm-text-2`; monospace data (IMEI, voltage) in `--tm-mono`.

### Top nav
**Fixed, 56-60px tall, solid `#0075FF`**, white text, white logo, `--tm-nav` type, 18px icons at
stroke 2. Identical across every product surface. The page header row sits below it: H2 title left,
utility buttons right. Navigation is **top-tab; there is no sidebar** in this product.

### Pagination / FAB
Active pagination tile: solid primary, white numeral. FAB: `radius 999px`, `shadow-lg`.

### Progress bars
Height 6-8px, `radius 999px`, track `--tm-divider`, fill semantic or the health gradient.

### Star ratings
Filled star `--tm-warning-500` `#F79009`, empty star `--tm-border-strong` `#D0D5DD`. **SVG stars —
never the star character** (Rule 7).

## 7. Iconography

- **Lucide**, standardized. `1.75-2px` stroke, rounded caps, `currentColor`.
- Sizes: top nav 18/2, button leading glyph 16/2, KPI tile glyph 18/2, table row 16/1.75,
  large status tile 20-24/2.
- Filled icons **only** for the small white glyph inside a colored status tile.
- Brand mark = the "location pin with ringed center dot". Mark alone below 28px; full wordmark at 28px+.
- On web prefer the `lucide-react` package over the CDN script (tree-shaken, typed, SSR-safe); on RN
  use `lucide-react-native`.
- Icons take semantic color tokens (`text-text-2`, `text-critical`), never a hex.

> **Open question inherited from the design project:** Lucide is a *substitution* — the icon set was
> matched visually, not confirmed against a codebase. If the project already bundles a different set
> (Heroicons outline, a custom set), that set wins; do not swap it. Flag the discrepancy once.

## 8. Copy & content rules

These come from the design system's CONTENT FUNDAMENTALS and are as binding as the visual tokens.
They apply to the **English source strings** in `t()` — see `18-working-language.md`.

- **Voice:** clinical, not cold. Short noun phrases, concrete numbers, no hype. Assumes domain knowledge.
- **Declarative, not instructive.** "Battery Failing" — not "Your battery is starting to show signs of
  failure, please check it soon."
- **Numbers first.** Every screen leads with a KPI, then the explanation.
- **Title Case** for buttons, nav items, page titles, KPI labels ("Export Dashboard", "Avg Fleet Score").
  **Sentence case** for prose and helper text. **ALL CAPS is never used** — not even for acronyms.
- **No pronouns.** "Avg Fleet Score", not "your fleet". No "we detected".
- **No exclamation points**, no "Let's…", no "Ready to…".
- **Numbers:** comma thousands separators (`1,275.68 kg`, `23,644`); unit trails with a space
  (`9,458 km`, `6h 58m`); percent with no space (`38%`, `+12%`); trend deltas read `+12% vs last`
  with a colored arrow icon, never an arrow character.
- **Domain vocabulary — lift verbatim, do not paraphrase:**
  Critical, Warning, Healthy, Optimal, Battery Optimal, Battery Failing, Parasitic Drain,
  Failing Alternator, Avg Fleet Health Score, Total Trips, Total Distance, Avg Trip Rating,
  Avg CO₂ Efficiency, Total CO₂ Emissions, Conversion Rate, Avg Stop Duration, Unique Vehicles,
  Total Stops, Total Pass-bys, Total Detections, Stop Duration.

## 9. What the system does NOT have

Reach for any of these and you are outside the system — stop and ask:

- Photographic or illustrated backgrounds, textures, noise, patterns. **Flat fills only.**
- Any gradient other than the health ramp.
- Frosted glass / `backdrop-filter`. The only transparency is the modal scrim
  `rgba(16,24,40,0.40)` (no blur) and the focus-ring glow.
- Inner shadows.
- Sidebars — navigation is top-tab.
- Left-border accent cards, gradient card headers.
- Bouncy/spring motion, scale-to-grow hovers, page transitions.
- A dark theme. **None is specified.** If a task asks for one, it is a design request, not an
  implementation detail — escalate rather than inventing an inverted palette.

## 10. Unspecified surfaces

The design project was derived from **three dashboard screens only**. Mobile, settings, empty states,
login and error states are **not specified**. Build them from the tokens and the component specs
above — same colors, same radii, same rhythm — and say in your summary that the surface had no
reference. Do not invent a new visual motif to fill the gap (`12-interactive-affordances.md`,
`11-responsive-defaults.md` and `09-data-listing.md` cover the behavioural defaults).

## 11. Checklist — run before calling any UI task done

- [ ] Zero raw hex / px / radius / shadow / font-family in components — every value is a token
- [ ] Page background `bg-bg` (`#F7F7F5`); cards white, borderless, `rounded-lg shadow-sm`, 20-24px padding
- [ ] Primary blue used only for nav, CTA, active state, links — not as a decorative accent
- [ ] KPI numerals weight 800; label → numeral → delta → bar order preserved
- [ ] Every status shows color **and** a Lucide glyph; tones from the semantic set
- [ ] Score bars use the five-stop health ramp with `Critical ← → Optimal` labels; no other gradient
- [ ] Focus ring present on every interactive element (`shadow-focus`), never `outline-none` alone
- [ ] Montserrat + JetBrains Mono only; no emoji, no Unicode pictographs, no icon font
- [ ] Copy is Title Case for labels, declarative, numbers-first, no pronouns, domain terms verbatim
- [ ] Any Figma value that had no token is listed in the summary as an explicit mapping
