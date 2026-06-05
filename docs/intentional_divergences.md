# Intentional Divergences (Type C)

Per PRD §7.6 / context.md §11.6. Code implements constitutional locks the xlsx may not yet reflect.

| Item | Classification | Notes |
|---|---|---|
| V4.113 cached vs Python (R4) | (C) spec-first | Entire model derived first-principles; xlsx is diagnostic reference only |
| CAE allocator F1–F6 (as-is R3) | (C) documented | F4 fixed U0; F1 cap-base fixed U1; F2 fixed U2; F5 fixed U3; F6 R14 fixed U4 in Python; xlsx cached CAE remains diagnostic |
| CAE F6 Conservation R14 (U4) | (C) Python-only fix | Python R14 includes facility flows + bridge/IPO reconciliation; V4.113 cached Conservation R14 still omits ODC facility (diagnostic) |
| CAE F5 seed + debt (U3) | (C) Python-only fix | Python folds ODC into spine (seed + alloc); Terafab repaid via chip transfer; V4.113 cached CAE still bypasses pool R134 (diagnostic) |
| CAE F1 cap-base (U1) | (C) Python-only fix | Python water-fill caps at R64–R66 growth slice; V4.113 cached CAE still uses pre-U1 deploy base (diagnostic) |
| CAE F2 two-resource (U2) | (C) Python-only fix | Python unifies cash+Gigabay in one pass; V4.113 cached CAE still uses independent softmax + pro-rata kg (diagnostic) |
| CAE F4 demand-spine (U0) | (C) Python-only fix | Python unifies R102≡R46; V4.113 cached CAE still shows inflated R99/R102 (diagnostic) |
| Cash Allocation Engine rows | (C) auto-triaged | Four-program two-resource fill diverges from cached CAE softmax/Level-2/pro-rata by design until U3–U4 |
| Group P&L 2025 vs xlsx cached | (C) auto-triaged | S-1 adherence path; full GAAP reconciliation xfails in Block B |
| Module outputs 2026+ | (C) auto-triaged | First-principles derivation on 2025–2040 horizon |
| Sprint 11f Option A (legacy) | (C) preregistered | Superseded by V4.113 CAE map; retained for V2.16 diagnostic runs |
| Starship R&D vs CapEx (D-A-03) | (C) documented | Port capitalizes Starship via vehicle build; S-1 expenses pre-commercialization R&D until 2H 2026. P1-4 adds explicit R&D memo line ($3,004M FY25). |
| Starshield scope (P1-10) | (C) S-1 scope adopted | Port Starshield scaled by `Starshield S-1 Government Connectivity scope factor` (~0.694) to align with S-1 Government Connectivity (~$1.75B) vs port mechanic (~$2.52B). Classified launch revenue remains in Customer Launch, not Starshield. Pending Vlad sign-off for final scope. |
