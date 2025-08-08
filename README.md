# OPEN HELIX — NBML v0.2.1

[![NBML Validation](https://github.com/Open-Helix/open-helix/actions/workflows/nbml-validate.yml/badge.svg)](https://github.com/Open-Helix/open-helix/actions/workflows/nbml-validate.yml)

**NBML** — Narrative Beat Markup Language (tiny interchange format).  
**HELIX-VAL** — structural validator CLI.  
**NVE** — CVE-style registry of narrative failure modes (with patches).  
**OMU** — public-domain NBML examples.

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
