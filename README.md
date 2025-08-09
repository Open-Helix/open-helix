# OPEN HELIX — NBML v0.2.1

[![NBML Validation](https://github.com/Open-Helix/open-helix/actions/workflows/nbml-validate.yml/badge.svg)](https://github.com/Open-Helix/open-helix/actions/workflows/nbml-validate.yml)

**NBML** — Narrative Beat Markup Language (tiny interchange format).  
**HELIX-VAL** — structural validator CLI.  
**NVE** — CVE-style registry of narrative failure modes (with patches).  
**OMU** — public-domain NBML examples.

NBML: A Tiny Open Standard for Story Structure
What is NBML?
NBML (Narrative Beat Markup Language) is a simple, human-readable format for representing the structure of a story — the beats, arcs, callbacks, stakes — in a way both humans and machines can read.

Think of it like JSON or YAML, but for stories: a single page of rules that makes narrative structure portable, validatable, and sharable across tools.

Why now?

We can generate text with AI, but there’s no shared way to represent structure — so every tool reinvents it, and outputs can’t be compared or improved systematically.

Without a common format, researchers can’t run apples-to-apples benchmarks on story coherence, and creative tools can’t exchange story structures.

NBML fills that gap.

What’s in the repo?

NBML Spec (v0.2) – the minimal rules for beats, arcs, callbacks.

HELIX-VAL Validator – checks any NBML file for structural integrity and outputs a score.

NVE Registry – a CVE-style catalog of common narrative failure modes, with reproducible fixes.

OMU Examples – public-domain stories converted into NBML so you can see it in action.

Why it matters

Interoperability: Any tool can import/export NBML.

Validation: Automatic checks catch structural flaws before they hit production.

Research: Reproducible datasets for AI narrative generation.

Collaboration: Writers, devs, and AI systems can speak the same structural language.

See it in action

View a public-domain story in NBML.

Run it through HELIX-VAL: get a structural score and a list of issues.

Apply NVE patches: watch the score go up.

Get involved

Use NBML in your project (see For Product Teams)

Join the NBML 1.0 Working Group

Submit to the 48-Hour Fix-My-Plot Clinic and see your story repaired in NBML.

Maintainer: Kevin Maistros · Colorgrade Pictures
📧 kevin.maistros@colorgrade.pictures
🌐 http://colorgrade.pictures



- Repo: https://github.com/Open-Helix/open-helix
- Website: http://colorgrade.pictures
- Maintainer: Kevin Maistros · Colorgrade Pictures · kevin.maistros@colorgrade.pictures

## Contents
- `specs/NBML_v0.2.md` — NBML spec
- `tooling/` — HELIX-VAL validator (CLI) and package
- `nvx/` — Narrative Vulnerabilities & Exposures entries
- `omu/` — NBML examples (Dracula, Alice, Sherlock)
- `docs/` — GitHub Pages site (serves spec/methods/product pages)
- `.github/` — CI/workflows and issue templates
- `METHODS.md`, `FOR_PRODUCT_TEAMS.md` — validator & integration docs
- `DATA_LICENSE.txt`, `LICENSE` — dual licensing

## Quickstart
```bash
pip install .[yaml]
helix-val validate omu/dracula.nbml.yaml --json
```

## License
- Code & spec: MIT (`LICENSE`)
- NBML datasets, OMU examples, clinic contributions: CC BY 4.0 (`DATA_LICENSE.txt`)
