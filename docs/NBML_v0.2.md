# NBML v0.2 — Narrative Beat Markup Language (Minimal Spec)

**Status:** Draft (v0.2) · **License:** MIT · **Scope:** Structure-level representation of long-form narrative.

## Purpose
NBML is a human-readable interchange format for **beats**, **arcs**, and **callbacks**. It enables validation, interoperability, and patching of common narrative failure modes.

## Format
Top-level keys:
- `version`: must be `NBML-0.2`
- `work_id`: string
- `logline`: string
- `genre`, `tone`, `themes`: optional
- `beats`: array (required)
- `arcs`: array (optional)
- `notes`, `metadata`: optional

Beat (required fields): `id`, `label`, `goal`, `conflict`, `stakes`, `callbacks[]`  
Arc (required fields): `character`, `start_trait`, `end_trait`, `pivot_beats[]`

## Minimal Checks (reference)
1. Schema & unique IDs
2. Callback Integrity (references earlier beats only)
3. Arc Consistency (pivot beats exist; trait changes)
4. Progression Presence (≥70% beats with goal+conflict+stakes)
5. Consequence Ladder heuristic (stakes escalate)
6. Minimum Beats (default ≥8)
7. No Orphan Callbacks / Arc Orphans
8. Labels non-empty; IDs unique
9. Extension hooks via `metadata`

## Scoring
The validator emits component scores [0–100] and a weighted total.

## Versioning
v0.2 remains minimal; community feedback will inform a 1.0 working group.

**Maintainer:** Kevin Maistros · Colorgrade Pictures · kevin.maistros@colorgrade.pictures
