# For Product Teams — 15-Minute NBML Integration

1) Import NBML (beats, arcs, callbacks) into your internal outline objects.
2) Export NBML with valid callbacks to earlier beats; include arcs if available.
3) Validate:
   ```bash
   pip install .[yaml]
   helix-val validate omu/dracula.nbml.yaml --json
   ```
Pass gate: total ≥ 70 and structure/callback/arc == OK.
