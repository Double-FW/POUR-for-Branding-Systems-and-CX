---
title: "POURS for branding systems and customer experience"
version: "2.0.0"
status: draft_for_review
license: MIT
language: en-GB
---

# POURS for branding systems and customer experience

POURS connects the functional foundations of accessibility with the quality of an experience and the promise a brand makes. It retains **Feeling Seen, Feeling Capable, Feeling Confident, Feeling Safe and Feeling Valued** and proposes **Satisfactory** as an additional Double FW experience principle.

WCAG continues to have four POUR principles. Accessibility and usability overlap; technical conformance alone cannot demonstrate customer satisfaction, brand alignment or particular feelings. This repository provides draft guidance for human review, not measured customer evidence, a compliance engine or an adopted organisational policy.

## Read in this order

| Document | Purpose |
| --- | --- |
| [1. Access, experience and brand promise](POURS_Access_Experience_and_Brand_Promise.md) | The framework and the five emotional passages, retained verbatim |
| [2. Satisfactory customer experience outcomes](Satisfactory_Customer_Experience_Outcomes.md) | Navigation, completion, time/effort, choice, content, engagement, recovery and dignity; Cognitive UX connections |
| [3. Brand values and inclusive experience research](Brand_Values_and_Inclusive_Experience_Research.md) | Turn actual brand values into testable commitments and accessible research |
| [4. POURS and EAA Annex I](POURS_and_EAA_Annex_I_Mapping.md) | Selective functional/emotional mapping with explicit legal boundaries |
| [5. Complaints, recovery and improvement](Complaints_Recovery_and_Continuous_Improvement.md) | Investigate dissatisfaction and barriers, repair, retest and learn |

The [original essay](The%20WCAG%20POUR%20principles%20reframed%20through%20emotional%20outcomes%20for%20branding%20systems.md) remains unchanged as historical context. The five guides above are the current interpretation. [AGENTS.md](AGENTS.md) provides contributor/agent guidance; [policies.yaml](policies.yaml) contains draft proposals parsed as data, never executed.

## Evidence boundaries

Keep functional access, satisfactory outcomes and reported emotional/brand experience separate. No complaints is not evidence of satisfaction. A satisfaction rating cannot override an unmet accessibility requirement. EAA complaints governance does not create a general satisfaction conformity test.

The guides link to public Double FW resources on Cognitive UX, EAA implementation, Synchronistic Design, programme runbooks and data ethics. They do not import or relicense those resources. No real participant, customer or complaint records are supplied. Publish methods and reviewed learning, not identifiable raw records.

## Hugging Face dataset and weekly updates

Destination: [GarethFW/POUR_for_Branding_Systems_and_CX](https://huggingface.co/datasets/GarethFW/POUR_for_Branding_Systems_and_CX).

GitHub is the authoring source. The existing workflow supports manual runs and Mondays at 07:23 UTC, subject to GitHub scheduling and inactivity rules. A change must reach the default branch before it can be published. Adding these documents does not require a new dataset, token or secret if the existing setup remains valid.

Version 2.0.0 expands the approved export list to all five guides. `documents` contains complete approved sources. `knowledge_chunks` contains exact sections of current Markdown guidance; the original essay and YAML are complete-document only to avoid duplicating the historical emotional text in the chunk view or fragmenting policy proposals. The two views overlap and must not be treated as independent examples when combined. No Q&A or participant results are generated.

The managed destination files are README.md, LICENSE, documents.jsonl, knowledge_chunks.jsonl, provenance.json, record_schema.json and validation_report.json. Unmanaged raw files remain and may be outdated. Provenance and validation reports describe a particular source snapshot and extraction checks, not legal, participant or brand validation. See [setup and verification](huggingface/SETUP.md).

## Review, contribution and licence

The five guides and policy changes are draft proposals for review. They require local owners, scope, research and adoption decisions before operational use. Changes to the export list require explicit review; missing approved sources, changed licence or invalid policy data block publication.

Double FW’s original material is under the [MIT licence](LICENSE). Retain its copyright and permission notice when distributing copies or substantial portions. Linked external sources keep their own terms. [CHANGELOG.md](CHANGELOG.md) records this update.

## About the author

Gareth Ford Williams is a senior leader in accessibility and inclusive design and co-founder of Double FW Ltd. His work spans accessibility, UX, technical standards, assistive technology and inclusive media. At the BBC, he led accessibility and UX work and chaired standards governance, translating research and policy into practical guidance.

## About Double FW Ltd

Double FW Ltd is a UK accessibility and inclusive design consultancy. It helps organisations build accessibility into strategy, governance, brands, products, content and services. Its public repositories provide practical guidance for people and AI-assisted workflows.
