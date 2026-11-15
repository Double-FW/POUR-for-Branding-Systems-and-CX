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
