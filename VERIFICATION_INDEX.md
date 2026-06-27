# Complete WCT Symbolic Verification Index

This index covers all 142 registered equation objects after applying `equations/derived_overrides.yaml` to `equations/full_registry.yaml`.

## Canonical navigation

- [Full corrected equation registry](https://github.com/rickyjreyes/geometry_of_resonance/blob/main/WCT_FULL_EQUATION_LIST_CORRECTED.md)
- [Master equation architecture](https://github.com/rickyjreyes/geometry_of_resonance/blob/main/WCT_MASTER_EQUATIONS_UPDATED.md)
- [Lean formal support](https://github.com/rickyjreyes/wct-lean)
- [Baseline checker assignments](equations/full_registry.yaml)
- [Active derived overrides](equations/derived_overrides.yaml)

A SymPy `PASS` is not a Lean proof or empirical validation.

> **Status precedence:** the `51 PASS / 32 CONDITIONAL / 23 DEFINITION / 36 OPEN` distribution embedded in the canonical equation document is the pre-derivation baseline. After the active derived overrides are applied, the effective distribution is `59 / 27 / 26 / 30`. The equation document remains canonical for equation text and assumptions; this index is canonical for the current effective SymPy classification.

## PASS — 59

`M2 M3 M4 M7 E1A E1B E2 E3 E4 E5 E6 E7 E8 E9 E10 E11 E12 E13 E14 E16 E17 E18 E20 E21 E24 E26 E28 E29 E30 E33 E37 E38 E45 E47 E49 E51 E53 E57 E58 E59 E61 E62 E64 E65 E67 E69 E81 CLE2 CLE4 CLE6 CLE7 CLE9 CLE10 G1 EX EY EZ CM9 CM11`

## CONDITIONAL — 27

`M1 M5 E15 E19 E22 E23 E31 E32 E40 E41 E48 E50 E54 E56 E66 E68 E70 E71 E72 E76 E80 CLE5 CLE8 FA TOP3 TOP7 CORR2`

## DEFINITION — 26

`M6A E25 E27 E35 E36 E39 E44 E52 E55 E60 E63 E73 E79 E82 CLE1 CLE3 CM12 CM13 CM16 CM18 TOP1 TOP2 TOP5 CORR1 CORR3 CORR4`

## OPEN — 30

`M6B M8 E34 E42 E43 E46 E74 E75 E77 E78 CM1 CM2 CM3 CM4 CM5 CM6 CM7 CM8 CM10 CM14 CM15 CM17 CM19 CM20 TOP4 TOP6 TOP8 TOP9 CORR5 CORR6`

## Effective totals

`59 PASS + 27 CONDITIONAL + 26 DEFINITION + 30 OPEN = 142`.

Use the canonical registry for equation text and assumptions, the YAML registries for checker assignments, and `wct-lean` for kernel-checked declarations.
