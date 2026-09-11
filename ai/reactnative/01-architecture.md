# RN Architecture, Build & State

> Shared principles (portable `_modules/`, component hierarchy, function minimalism) live in
> `ai/shared-fe/`. This file covers the **RN/Expo-specific** setup.

## Tech Stack
- **React Native 0.79** with **Expo ~53** (SDK 50+ for built-in Expo Router)
- **React 19**, **TypeScript** preferred for all new code
- **TanStack Query 5** — data fetching, caching, global cache
- **Zod** + **React Hook Form** + `@hookform/resolvers` — validation & forms
- **React Context Provider** for global state (no Zustand)
- **Expo Router** — file-based navigation (built in; no extra install)
- **AsyncStorage** — persistent client state (replaces `localStorage`)
- Animations — **optional**; Moti / React Native Reanimated only when a screen genuinely needs them (not a default dependency — see `02-styling`)

## Dependency policy

> **Build our own shared/common components (`Base*`, `Col`, `Row`, `TextPrimary`); minimize dependence on
> external UI packages.** Reach for a library only when the feature genuinely needs native/platform
> plumbing we should not reinvent.

**Preferred libraries** — when a feature needs one of these areas, PREFER these exact packages.

The **Platform** column matters: this KB is written Expo-first, but several entries are Expo-only and
have a different RN-CLI equivalent. *Both* = one package serves Expo and bare RN CLI alike.

| Area | Platform | Package |
|------|----------|---------|
| Safe-area insets | Both | `react-native-safe-area-context` |
| Persistent key-value storage | Both | `@react-native-async-storage/async-storage` |
| SVG / vector graphics / icons | Both | `react-native-svg` |
| OTP / verification code input | Both | `react-native-otp-entry` |
| In-app browser (OAuth, ToS / policy links) | Both | `react-native-inappbrowser-reborn` |
| Image pick + crop | Both | `react-native-image-crop-picker` |
| Image resize / compress before upload | Both | `@bam.tech/react-native-image-resizer` |
| Bottom-sheet modal | Both | `react-native-modalize` — read the caveat below |
| Splash screen | Expo | `expo-splash-screen` — RN CLI: `react-native-bootsplash` |
| Status bar | Expo | `expo-status-bar` — RN CLI: RN's built-in `StatusBar` |
| File-based navigation | Expo | `expo-router` — RN CLI: `@react-navigation/native-stack` + `react-native-screens` |

### Notes on the media / browser / modal entries

- **All four are native modules.** On Expo they require a **development build** — none of them work in
  Expo Go. On RN CLI they need a `pod install` plus a rebuild, not just a Metro restart.
- **`react-native-inappbrowser-reborn`** keeps OAuth and policy links inside the app, so the session
  cookie and the back-navigation stay ours instead of handing the user to Safari/Chrome. If a project is
  already on Expo SDK and needs nothing beyond "open a URL in a sheet", `expo-web-browser` is the
  lighter choice — prefer the reborn package when you need the full `openAuth` flow or custom chrome.
- **`react-native-image-crop-picker`** is preferred over `expo-image-picker` because it ships a real
  native cropping UI. Pair it with the resizer rather than uploading the cropper's output directly.
- **`@bam.tech/react-native-image-resizer`** is the maintained fork of the abandoned
  `react-native-image-resizer` — use the `@bam.tech/` scope, never the unscoped name. Always resize
  before upload; a modern phone camera produces 4–12 MB images that do not belong on the wire.
- **`react-native-modalize` caveat (verified 2026-09-12):** the last npm release is `2.1.1`, published
  **2022-08-10**, and it peers on `react-native-gesture-handler`. That predates the New Architecture
  becoming the default, so on a Fabric-only project (RN 0.76+ with `newArchEnabled=true`) verify it
  actually renders before committing to it. If it does not, `@gorhom/bottom-sheet` is the maintained
  equivalent — it needs `react-native-gesture-handler` **and** `react-native-reanimated`. Either way a
  bottom sheet pulls in gesture-handler, which is otherwise NOT required by `native-stack`.

Animation libraries (Moti / Reanimated) are **not** on the preferred list — treat them as optional add-ons,
consistent with minimizing external deps. **Exception:** some preferred native modules force
`react-native-worklets` / `react-native-reanimated` in as a hard peer — `react-native-executorch` requires
worklets, and `react-native-keyboard-controller` requires Reanimated. When a required dependency pulls
them in, that is not a violation of this policy.

## Modular Structure (`_modules/` — RN flavor)

```
src/ (or root)
├── index.js             # Entry point
├── App.tsx              # Root navigator / provider mount (routing only)
├── config.js            # Runtime configuration
├── _modules/            # Framework-agnostic business logic (100% portable)
│   ├── _api/            # baseFetch, apiClient[Domain], apiUrl, utilsApi
│   ├── common/
│   │   ├── components/  # Col, Row, TextPrimary, Base* components
│   │   ├── context/     # React Context providers (Auth, etc.)
│   │   ├── hooks/       # Reusable hooks
│   │   ├── schemas/     # Zod schemas
│   │   └── utils/       # Pure utilities
│   ├── config/          # Configuration constants
│   ├── screens/         # Screen components (ALL business logic)
│   │   └── [Name]/[Name]Screen.tsx + components/
│   └── values/          # enums, theme, routes, dummy data
├── app/                 # Expo Router routes (routing ONLY) — see 03-navigation
└── services/            # Native/platform services (Audio, WebSocket, camera, …)
```

**Routing layer is thin.** `app/` (Expo Router) or `App.tsx` files only import and render a Screen from
`_modules/screens/`. All hooks, state, and logic live in the Screen. (Same rule as web — see
`ai/shared-fe/01`.)

## Build & Run

```sh
yarn install
npx expo start --dev-client        # dev server (custom dev client)

yarn android                       # expo run:android
yarn ios                           # expo run:ios

# Build a dev client (REQUIRED — app uses native modules, cannot use Expo Go)
npx eas build --platform android --profile development
npx eas build --platform ios     --profile development
```

> **Cannot run in Expo Go** when native modules are present — build a custom dev client via EAS.

## State Management
- **TanStack Query** — API/server state + global cache (`staleTime: Infinity` for near-static data).
- **React Context Provider** — global app state (auth, settings, theme); no external store.
- **React Hook Form** — form state.
- **AsyncStorage** — persistent client state (async; see `04-data-and-storage.md`).
- **`useState`** — local UI state only.

Data flow: `baseFetch → apiClient* → useQuery/useMutation → Screens`, with Context for cross-cutting
global state.

## Environment Configuration
- Runtime config in `config.js` (e.g. `API_KEY`, `MODEL_NAME`, audio toggles).
- **Client-readable env vars must be prefixed `EXPO_PUBLIC_`** (e.g. `EXPO_PUBLIC_API_BASE_URL`).

## Enums & Constants (RN specifics)
Follows `ai/shared-fe/04` (E-prefixed enums, const objects over string literals). RN adds:
- **`EAsyncStorageKey`** — typed keys for AsyncStorage (`AUTH_TOKEN`, `USER_PREFS`, …).
- **Route constants** in `_modules/values/routes.ts` (Expo Router paths — see `03-navigation`).
- **Theme-coupled enum maps** (label/color per enum value) reference `values/theme` — see `02-styling`.

```ts
// _modules/values/enums.ts
export enum EAsyncStorageKey {
  AUTH_TOKEN    = 'auth_token',
  USER_PREFS    = 'user_prefs',
  GUEST_CART_ID = 'guest_cart_id',
}
```

## RN house rules
- Prefer **TypeScript** — do not create new `.js` files.
- Do **not** use a barrel/`index` file to re-export many components.
- Always `StyleSheet.create({})` — never inline style objects (see `02-styling`).
