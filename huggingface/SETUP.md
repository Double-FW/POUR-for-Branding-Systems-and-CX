# Weekly POUR for Branding Systems and CX updates

Source: https://github.com/Double-FW/POUR-for-Branding-Systems-and-CX

Destination: https://huggingface.co/datasets/GarethFW/POUR_for_Branding_Systems_and_CX

The destination is fixed in export-config.json. No HF_DATASET_ID variable is needed.
Save a destination-scoped Hugging Face token as repository secret HF_TOKEN, then
create .github/workflows/huggingface-sync.yml from WORKFLOW_TO_COPY.txt in the
setup download. Run manually once and check the result; weekly runs are Mondays
at 07:23 UTC. Never commit credentials; use the token copy button.

All approved source files are required. Review new or renamed sources in the
export list. YAML definitions are safely parsed as source proposals, not executed
as rules. The Satisfactory extension remains separate from official WCAG POUR.


## Framework version 2.0.0 maintenance

This update uses the existing repository, destination and HF_TOKEN secret. Do not create a new token merely for this content update. The source guard and weekly/manual workflow are unchanged.

The approved list now contains README, AGENTS, the original essay, policies and all five current guides. Every source and LICENSE is required. YAML and the historical essay are complete-document only; current Markdown guides also produce exact section records. Dataset views overlap.

Run checks from the repository root after committing source changes:

```bash
python -m pip install -r huggingface/requirements.txt
python -m unittest discover -s tests -v
python scripts/export_huggingface.py --output ../pours-export-check
```

The export must be outside the source checkout. The exporter reads committed HEAD, so uncommitted edits are not a publication preview. Check the generated dataset card and validation report. The tests use mocked publication; they make no live dataset writes and do not establish legal compliance or measured customer outcomes.

After the reviewed change reaches main, open Actions → the existing Hugging Face sync workflow → Run workflow → select main → Run workflow. Check the completed run, then the destination dataset's files/history and provenance source commit. Confirm version 2.0.0 and that documents contains all five guides while knowledge_chunks excludes the legacy essay and YAML. Keep any unmanaged raw files under separate review; the workflow does not synchronise them.

If publication fails, read the failing step before changing permissions or recreating credentials. Never put a token in a file, issue, pull request, screenshot or chat. Successful local extraction is not a successful live publication.
