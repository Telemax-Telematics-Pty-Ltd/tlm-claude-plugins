#!/usr/bin/env node
// PostToolUse hook — lints the file Claude just edited against the tlm-fe-coding
// HARD RULES that are mechanically detectable, and feeds any hits back so Claude
// self-corrects in the same turn.
//
// Advisory, never blocking: PostToolUse runs AFTER the write, so this cannot undo
// an edit. It emits hookSpecificOutput.additionalContext (the documented channel
// that reaches Claude's context without surfacing as an error to the user).
//
// Silent unless it finds something. High-signal rules only — a noisy linter gets
// turned off, so every rule here is one the plugin states as a hard rule, with
// the well-known false-positive sites (Base* primitives, token files, the Prisma
// singleton, comments) excluded.

import fs from 'node:fs'
import path from 'node:path'
import { readStdinPayload, delegateToVendored, emitContext, toPosix } from './lib/hook-io.mjs'

const { raw, json: input } = readStdinPayload()
const file = input?.tool_input?.file_path
if (!file) process.exit(0)

// The project's vendored rules are the live source: if this repo carries its own
// copy of this hook, that copy decides — a rule added there must be enforced now,
// not after the PR merges.
delegateToVendored({
  selfUrl: import.meta.url,
  startDirs: [path.dirname(file), input?.cwd, process.env.CLAUDE_PROJECT_DIR],
  raw,
})
try {
  if (!fs.statSync(file).isFile()) process.exit(0)
} catch {
  process.exit(0)
}

// Path rules below are written in posix form; a Windows path must be normalized
// first or every one of them silently misses.
const posix = toPosix(file)
const base = path.basename(posix)

// Only TypeScript / TSX. Skip declarations, tests, stories, generated deps.
if (!/\.tsx?$/.test(posix)) process.exit(0)
if (
  /\.d\.ts$/.test(posix) ||
  /\.(test|spec)\.tsx?$/.test(posix) ||
  /\.stories\.tsx$/.test(posix) ||
  posix.includes('/node_modules/') ||
  posix.includes('/.next/')
) {
  process.exit(0)
}

// Per-file exemptions for rules that legitimately allow the pattern.
// Base* primitives are the ONLY layer allowed raw/semantic DOM, and the raw-HTML
// rule is JSX-only.
const skipHtml = base.startsWith('Base') || !posix.endsWith('.tsx')

// token/theme/config files are where raw design values are SUPPOSED to live — the
// Telemax Design System mirror, the Tailwind config, and the RN theme constants module
// are the ONE place per platform that may spell a hex, a px size, a radius or a shadow.
const skipHex =
  posix.includes('tailwind.config') ||
  posix.includes('telemax-tokens') ||
  /[Tt]heme/.test(posix) ||
  /[Cc]olors/.test(posix) ||
  posix.includes('/config/') ||
  posix.includes('/theme/')

// the singleton file is the one place `new PrismaClient()` belongs
const skipPrisma = ['prisma.ts', 'db.ts', 'client.ts', 'prismaClient.ts', 'prisma.server.ts'].includes(base)

let source
try {
  source = fs.readFileSync(file, 'utf8')
} catch {
  process.exit(0)
}
// Tolerate CRLF so a checkout with Windows line endings lints the same.
const lines = source.split('\n').map((l) => l.replace(/\r$/, ''))

const findings = []

// scan(pattern, message) — record "file:line — message" for each non-comment match.
function scan(pattern, message) {
  const re = new RegExp(pattern)
  lines.forEach((line, i) => {
    if (!re.test(line)) return
    const trimmed = line.replace(/^\s+/, '')
    // comment line — not a real violation
    if (trimmed.startsWith('//') || trimmed.startsWith('*') || trimmed.startsWith('/*')) return
    findings.push(`  - ${file}:${i + 1} — ${message}\n`)
  })
}

// --- universal TS rules ----------------------------------------------------
scan(
  '(^|[^A-Za-z0-9_])as any([^A-Za-z0-9_]|$)',
  'as any — fix the root cause with a proper type/generic/type-guard (as unknown as T only as a commented last resort)'
)
scan(
  '@ts-(ignore|expect-error)',
  '@ts-ignore / @ts-expect-error — avoid; if truly unavoidable add a comment explaining why'
)

// --- styling ---------------------------------------------------------------
if (!skipHex) {
  scan(
    '(\\[#[0-9a-fA-F]{3,8}\\]|#[0-9a-fA-F]{6}([^0-9a-fA-F]|$)|#[0-9a-fA-F]{3}([^0-9a-fA-F]|$))',
    'hardcoded hex color — move it to a design token (Tailwind @theme / theme constants) and use it by name'
  )

  // --- Telemax Design System: arbitrary values off the token scale ----------
  // ai/shared-fe/19-design-system.md Rule 1. Each of these is a value the system
  // already has a token for, so an arbitrary value is a silent divergence.
  scan(
    'rounded-\\[',
    'arbitrary border radius — Telemax radii are tokens: rounded-md (10px inputs/buttons), rounded-lg (12px cards), rounded-pill (999px). See ai/shared-fe/19-design-system.md §2.6'
  )
  scan(
    'shadow-\\[',
    'arbitrary box-shadow — use the elevation tokens shadow-xs / shadow-sm (cards) / shadow-md / shadow-lg / shadow-focus. See ai/shared-fe/19-design-system.md §2.7'
  )
  scan(
    '(^|["\\s`])-?(p|px|py|pt|pb|pl|pr|m|mx|my|mt|mb|ml|mr|gap|gap-x|gap-y|space-x|space-y)-\\[[0-9.]',
    'arbitrary spacing — Telemax is a 4px grid and it IS Tailwind\'s scale (p-6 = 24px, p-10 = 40px). Use the numbered utility. See ai/shared-fe/19-design-system.md §2.5'
  )
  scan(
    '(^|["\\s`])text-\\[[0-9.]',
    'arbitrary font size — use a type token: text-h1/h2/h3, text-kpi, text-body, text-label, text-caption, text-micro, text-nav. They carry size + line-height + weight together. See ai/shared-fe/19-design-system.md §2.4'
  )
  scan(
    '(^|["\\s`])font-\\[',
    'arbitrary font-family — the Telemax system ships Montserrat (font-sans) and JetBrains Mono (font-mono) only. See ai/shared-fe/19-design-system.md Rule 8'
  )
  // Stock Tailwind palette: renders fine, but it is NOT the Telemax palette. The
  // classic tell is bg-gray-50 as the page and bg-blue-500 as "primary".
  scan(
    '(^|["\\s`:])(bg|text|border|ring|fill|stroke|from|via|to|divide|outline|shadow|accent|decoration|placeholder|caret)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-(50|[1-9]00|950)([^0-9]|$)',
    'stock Tailwind palette class — not the Telemax palette. Use the semantic tokens: bg-bg (page #F7F7F5), bg-surface (card), text-text-1/2/3/4, border-border, bg-primary, text-success/warning/critical. See ai/shared-fe/19-design-system.md §2'
  )
}

// A focus ring is never removed. File-level guard rather than per-line so an element
// that restores the ring elsewhere in the same file is not flagged.
if (!/shadow-focus|focus-visible:|focusVisible/.test(source)) {
  scan(
    'outline-none',
    'outline-none with no replacement focus ring in this file — add focus-visible:shadow-focus (the 4px rgba(0,117,255,0.20) ring). Removing focus indication is a hard violation. See ai/shared-fe/19-design-system.md Rule 6'
  )
}

// No emoji, no Unicode pictographs — they render differently per OS and cannot take a
// stroke-width. Arrows (← → used in the "Critical ← → Optimal" label) and the middot
// separator used by joinWith are deliberately NOT matched.
scan(
  '([\\u2600-\\u27BF]|\\u2B50|\\u25B2|\\u25BC|\\u25CF|\\uFE0F|[\\uD83C-\\uDBFF][\\uDC00-\\uDFFF])',
  'emoji / Unicode pictograph in the UI — the Telemax system uses Lucide SVG icons only (star, warning triangle, check, status glyphs included). See ai/shared-fe/19-design-system.md Rule 7'
)

// --- component hierarchy ---------------------------------------------------
if (!skipHtml) {
  scan(
    '<(div|span|p)( |>|/|$)',
    'raw HTML (<div>/<span>/<p>) — use Col / Row / TextPrimary; only Base* primitives may render raw DOM'
  )
}

// --- navigation ------------------------------------------------------------
scan(
  'router\\.push\\(',
  'router.push — navigate via <Link> (web) / router.navigate (RN); router.push/replace is for post-action redirects only'
)

// --- contracts: responses are parsed, not cast ------------------------------
scan(
  '\\.json\\(\\)\\s*\\)?\\s*as\\s+[A-Za-z_$(]',
  'response cast (`.json() as T`) — parse it with the Zod schema at the service boundary (schema.parse / safeParse); the type comes from z.infer. See ai/shared-fe/15-zod-contract-first.md'
)

// --- page-router / prisma hard rules --------------------------------------
scan(
  '(^|[^A-Za-z0-9_])getServerSideProps([^A-Za-z0-9_]|$)',
  'getServerSideProps — Page Router fetches via useQuery[Entity] hooks, not getServerSideProps'
)
if (!skipPrisma) {
  scan(
    'new PrismaClient\\(',
    'new PrismaClient() outside the singleton — import the shared Prisma singleton instead of instantiating per request'
  )
}

// Nothing to say -> stay silent.
if (findings.length === 0) process.exit(0)

emitContext(
  'PostToolUse',
  `tlm-fe-coding hard-rule check on ${file} flagged:
${findings.join('')}
Fix these in the file you just edited before continuing. If a flag is a genuine, justified exception, say so explicitly rather than leaving it silent.`
)
