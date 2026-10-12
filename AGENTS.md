---
title: "Agent Guide: POUR for Branding Systems & CX"
version: "0.1.0"
author: "Double-FW"
date: "2026-10-12"
license: "MIT"
language: "en"
repository: "Double-FW/POUR-for-Branding-Systems-and-CX"
artifact_type: "agent_guide"
use_case: "brand-accessibility-agent, escalation-routing"
conceptual_entities:
  - POUR_emotional_translations
  - policy
  - escalation
  - audit_log
  - prompt_template
  - decision_state
---

# Agent Guide

This repository captures a brand-and-customer-experience interpretation of the WCAG POUR principles. Its purpose is to frame accessibility not as compliance alone, but as emotional trust, belonging, clarity, and confidence in every user interaction. The work emphasizes that people feel included when products, content, and service experiences are designed with dignity and intent.

## Repository purpose

The core idea is that accessible design should be felt in the same way a strong brand promise is felt: users should feel seen, capable, confident, safe, and valued. This repository reframes WCAG's principles through emotional outcomes that matter in brand and customer experience.

The work centers on these emotional translations:

- Feeling Seen (Perceivable)
  - People can access and recognize content without being excluded by format, context, or sensory barriers.
- Feeling Capable (Operable)
  - People can act, navigate, and complete tasks without unnecessary friction or invisible blockers.
- Feeling Confident (Understandable)
  - People understand what is happening, what to do next, and why choices are being presented.
- Feeling Safe (Robust)
  - People trust that the system will hold up across tools, contexts, and changing circumstances.
- Feeling Valued (Satisfactory)
  - People feel respected, included, and intentionally considered rather than merely accommodated.

## Machine-readable rules and metadata

The repository should be readable both by humans and by automation. The following YAML block defines the minimal policy metadata an agent can parse reliably before making recommendations or escalating an issue.

```yaml
policies:
  - id: "p-perceivable-01"
    title: "Perceivable"
    description: "Users must be able to recognize and access content without exclusion by sensory or format barriers."
    severity: "high"
    categories: ["content", "brand", "accessibility"]
    triggers:
      - "missing_alt_text"
      - "missing_captions"
      - "content_only_in_visual_format"
    actions:
      - type: "suggest_fix"
        template: "Provide accessible alternatives such as text, transcripts, captions, or structured descriptions."
      - type: "escalate"
        when: "severity == 'high' and impact == 'critical'"
        escalation_level: "human_accessibility_reviewer"

  - id: "p-operable-01"
    title: "Operable"
    description: "Users must be able to navigate and act without unexpected barriers."
    severity: "medium"
    categories: ["interaction", "navigation", "experience"]
    triggers:
      - "keyboard_inaccessible_controls"
      - "focus_trap"
      - "unlabeled_action"
    actions:
      - type: "suggest_fix"
        template: "Ensure controls are keyboard usable, clearly labeled, and navigable without hidden traps."

  - id: "p-understandable-01"
    title: "Understandable"
    description: "People should understand the context, actions, and decisions in the experience."
    severity: "medium"
    categories: ["copy", "interface", "decision_support"]
    triggers:
      - "ambiguous_state"
      - "unclear_error"
      - "misleading_label"

  - id: "p-robust-01"
    title: "Robust"
    description: "Systems should remain reliable across devices, assistive technologies, and changing conditions."
    severity: "high"
    categories: ["technical", "resilience", "trust"]
    triggers:
      - "technical_regression"
      - "incompatible_assistive_technology"
      - "inconsistent_behavior_across_contexts"

  - id: "p-satisfactory-01"
    title: "Satisfactory"
    description: "The experience should feel respectful, inclusive, and emotionally safe."
    severity: "low"
    categories: ["brand", "cx", "inclusion"]
    triggers:
      - "tone_undermines_trust"
      - "excluded_language"
      - "friction_without_support"
```

For automation, the repository can also provide a minimal JSON object to validate rules before execution:

```json
{
  "schema_version": "1.0",
  "repository": "Double-FW/POUR-for-Branding-Systems-and-CX",
  "entity_types": [
    "policy",
    "prompt_template",
    "audit_log",
    "escalation",
    "decision_state"
  ],
  "required_fields": [
    "id",
    "title",
    "description",
    "severity",
    "actions"
  ]
}
```

## Prompt templates and response examples

The agent should emit brief, consistent, and templated responses that remain empathetic and policy-aware.

```markdown
### Template: issue summary
Prompt:
"User reports: {user_issue}. Check applicable POUR principles and provide a short summary, risk level, and recommended remediation."

Response:
"{risk_level}: The issue aligns with {policy_name}. Recommended fix: {recommended_fix}. Impact: {impact_summary}."
```

```markdown
### Template: escalation note
Prompt:
"Escalation {escalation_id}: {policy_name} triggered by {trigger}. Provide a one-paragraph summary for a reviewer and a human-readable next step."

Response:
"This issue affects {user_group_or_context}. The current behavior may reduce trust and accessibility because {reason}. Recommended next step: {next_step}."
```

```markdown
### Template: user-facing acknowledgement
Prompt:
"Draft a brief, empathetic message for a user experiencing accessibility friction in {feature}."

Response:
"We’re sorry that {feature} caused friction. We’re reviewing this issue and will work to improve accessibility and clarity. If this continues, please share {support_contact}."
```

## Observability hooks and logging requirements

Every escalation and non-trivial decision should be auditable. Logging must be designed to support review, diagnostics, and governance without exposing sensitive information.

### Required observability fields

```json
{
  "timestamp": "ISO-8601",
  "agent_id": "string",
  "event_type": ["evaluation", "response", "escalation", "audit", "error"],
  "policy_id": "string",
  "trigger": "string",
  "escalation_id": "string",
  "risk_level": ["low", "medium", "high", "critical"],
  "decision": "string",
  "summary": "short human-readable explanation",
  "redacted_fields": ["email", "phone", "user_id"],
  "retention_class": ["short", "standard", "archive"]
}
```

### Logging rules

- Log the time, policy context, escalation ID, and decision outcome for every issue evaluation.
- Keep logs concise and structured so they can be reviewed programmatically.
- Redact or hash direct personal data before storage.
- No raw user content should be retained unless explicitly required and approved.
- Escalations require a clear reviewer trail and a reason code.

### Redaction policy

- Replace email addresses with hashed tokens.
- Replace phone numbers, addresses, and direct customer identifiers with placeholders.
- Store only summaries or structured metadata when the original content is unnecessary.
- Use reversible encryption only when strictly required by an approved policy.

### Retention policy

- Standard operational logs: 365 days.
- Escalation records: 1095 days unless otherwise required by policy or legal review.
- Audit exports should be CSV or JSONL and include redaction metadata.

## Quick-start checklist

Use this checklist before creating or revising accessibility guidance or escalating an issue.

- [ ] Confirm the issue is framed through the relevant POUR emotional outcome.
- [ ] Check whether the issue is content, interaction, understandability, resilience, or trust-related.
- [ ] Identify the affected policy and severity.
- [ ] Decide whether an automated response is sufficient or a human escalation is needed.
- [ ] Log the event with a policy ID, timestamp, risk, and decision summary.
- [ ] Ensure no sensitive personal information is stored in raw form.
- [ ] Verify the recommendation aligns with the repository's brand-and-CX lens.

## Minimal decision flowgraph

The agent can operate using a simple, programmatic decision flow:

```text
START
  |
  v
Normalize issue and context
  |
  v
Match against policy rules
  |
  +--> No match ------------------> Auto-response with generic guidance
  |
  v
Policy match
  |
  +--> High or critical severity --> Escalate to human reviewer + log audit record
  |
  +--> Medium severity ----------> Generate guided response + log audit record
  |
  +--> Low severity -------------> Auto-respond with safe, brief guidance
  |
  v
END
```

A state-machine equivalent for code or automation:

```yaml
states:
  - id: ingest
    transitions:
      - condition: "issue.valid"
        to: classify
      - condition: "!issue.valid"
        to: safe_default

  - id: classify
    transitions:
      - condition: "policy_match and severity in ['high','critical']"
        to: escalate
      - condition: "policy_match and severity == 'medium'"
        to: guided_response
      - condition: "policy_match and severity == 'low'"
        to: auto_response
      - condition: "!policy_match"
        to: generic_response

  - id: escalate
    actions:
      - "assign_reviewer"
      - "write_audit_log"

  - id: guided_response
    actions:
      - "emit_templated_response"
      - "write_audit_log"

  - id: auto_response
    actions:
      - "emit_templated_response"
      - "write_audit_log"

  - id: generic_response
    actions:
      - "emit_generic_guidance"
      - "write_audit_log"
```

## Version, changelog, and review metadata

The repository should maintain version metadata that can be checked automatically before rules are trusted.

```yaml
version: "0.1.0"
changelog:
  - version: "0.1.0"
    date: "2026-10-12"
    summary: "Added machine-readable policy metadata, prompt templates, observability requirements, quick-start checklist, decision flow, and audit/review metadata."
review:
  last_reviewed: "2026-10-12"
  reviewed_by: "Double-FW"
  required_approvers:
    - "accessibility-reviewer"
    - "content-editor"
  review_frequency_days: 180
```

## Core files

- `README.md` — introductory overview of the project and its intent.
- `The WCAG POUR principles reframed through emotional outcomes for branding systems.md` — the central conceptual document.
- `LICENSE` — MIT licensing information.

## Editorial guidance

When editing or extending this repository, maintain the following principles:

1. Keep the emotional framing central.
   - Accessibility is not only functional; it shapes how people feel about a brand and whether they trust it.

2. Connect accessibility to brand and CX.
   - The repository argues that marketing promises and lived experience must align.

3. Favor inclusive, human language.
   - Use wording that emphasizes dignity, belonging, clarity, and trust.

4. Stay grounded in the POUR lens.
   - Preserve the connection between WCAG concepts and emotional outcomes.

5. Avoid reducing the work to checklists or legal compliance alone.
   - The value of the framework is its emotional and strategic impact on customers.

## Working style

- Write clearly and accessibly.
- Use plain language grounded in real customer experience.
- Prefer examples and framing that connect brand, accessibility, and inclusive service design.
- Preserve the repository's voice: practical, reflective, and intentionally human-centered.

## Intended outcome

This repository is meant to help teams design brand and customer experiences that feel welcoming, usable, clear, reliable, and respectful. In this framing, accessibility becomes part of brand integrity, not a separate compliance exercise. The goal is not only to remove barriers, but to make people feel seen, capable, confident, safe, and valued.

## Automation notes

- Validate the YAML front matter before using repository guidance in an automated workflow.
- Prefer structured metadata over raw prose when building agents, QA tooling, or policy checks.
- Maintain version metadata and a simple changelog so future automation can decide whether rules are trustworthy and current.
- Treat the emotional outcomes as the primary conceptual lens; technical compliance remains important, but not sufficient on its own.
