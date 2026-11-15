---
title: "Satisfactory: customer experience outcomes"
version: "2.0.0"
status: draft_for_review
license: MIT
language: en-GB
---

# Satisfactory: customer experience outcomes

**Satisfactory is a proposed Double FW addition to POUR, not a fifth WCAG principle or a general EAA satisfaction requirement.** It means that people can achieve their intended outcomes in a way that meets their needs and reasonable expectations without sacrificing dignity, identity, privacy or control. Read this with the [framework](POURS_Access_Experience_and_Brand_Promise.md) and [research guide](Brand_Values_and_Inclusive_Experience_Research.md).

## Define the task before the measure

Name the real outcome, starting conditions, route, relevant product version and correct end state. “Clicked submit” is not evidence that a booking exists, a payment is correct or a cancellation took effect. Include discovery, authentication, support, confirmation and later changes when these are necessary parts of the journey.

Agree success criteria with affected people and the service owner before a study. Do not invent universal acceptable times, completion percentages or satisfaction thresholds. Record where agreement is provisional and why. Assistance chosen by the participant can be a valid preference; assistance forced by an inaccessible route exposes a barrier. Keep those cases distinct.

## Outcomes and evidence

The SX identifiers below are local research categories. They do not replace WCAG criteria, EAA clauses, Cognitive UX CP identifiers or the EAA repository’s IDSO outcomes.

| ID | Outcome | Observe or ask | Interpretation safeguard |
| --- | --- | --- | --- |
| SX01 | Navigation and orientation | Can the person find the next step, recognise their location and return without losing work? | Record detours and uncertainty; page arrival alone is insufficient |
| SX02 | Correct task completion | Verify the intended end state, errors, abandonment and assistance | Include people unable to start; report independent and assisted outcomes separately |
| SX03 | Acceptable time and effort | Record active time, waiting, rest, retries and support queues separately | Faster is not always better; preserve time to understand and choose |
| SX04 | Choice and preferences | Can the person discover, use, change and retain relevant settings, including declining them? | Options must be meaningful, accessible and privacy-preserving |
| SX05 | Content consumption and understanding | Can the person obtain the relevant meaning in their chosen format and explain a consequential decision? | Recall tests alone can add an unrelated memory demand |
| SX06 | Voluntary engagement | Can they participate, pause, disengage and return on their own terms? | Longer visits, more clicks and repeat contact may indicate friction |
| SX07 | Continuity and recovery | After an interruption, error or handover, can they identify the state and continue safely? | Record lost work, repeated disclosures and any unresolved consequences |
| SX08 | Dignity, identity and support | Was support respectful, effective and available through a usable route? | Do not require a diagnosis or repeated proof of disability to describe a barrier |
| SX09 | Satisfaction and expectation | What met or fell short of the person’s needs, expectations and priorities? | Ratings do not override failed requirements or prove brand loyalty |

## Cognitive UX connections

Use the [owning Cognitive Design Principles](https://github.com/Double-FW/Cognitive-UX-Design/blob/main/Cognitive%20Design%20Principles.md) for definitions and revisions. The following is a research cross-reference, not a new version of those principles.

| Cognitive UX identifier | Application to satisfactory experience |
| --- | --- |
| CP01: standard elements | Familiar controls and consistent states support navigation and resumption |
| CP02: affordances and signifiers | People can discover what actions are possible and what their results mean |
| CP03: simplicity | Remove unnecessary demands while preserving meaningful options and task context |
| CP04: clear communication | Explain choices, consequences and errors without blame |
| CP05: redundancies | Offer equivalent cues and formats without overwhelming people with simultaneous output |
| CP06: patterns | Group and structure information so relationships can be recognised |
| CP07: recognition rather than recall | Keep relevant context available across steps and interruptions |
| CP08: variable stimuli and pop-out | Use controlled salience for important information; avoid attention capture and unstable layouts |
| CP09: feedback and notification | Distinguish pending, successful and failed actions and retain consequential feedback |
| CP10: user control and choice | Support pace, presentation, preferences and safe recovery |

A proposed change should name the demand it removes and how its effect will be observed. Cognitive accessibility is not a reason to hide information, force one mode or assume a diagnosis from behaviour.

## Measurement plan

For completion, state the denominator: invited, started, unable to start, completed correctly, completed with chosen support, completed only with forced support, incorrect result and abandoned. Define mutually exclusive primary outcome categories, then report assistance and barriers as additional attributes. Do not silently exclude difficult cases to improve a success rate.

For time, define start and stop events and report non-completion separately. Describe differences in task, technology, pace and assistance before comparing groups. An average can hide a severe barrier; show the distribution or individual cases where privacy permits. Do not rank disability groups as inherently slower.

For satisfaction, ask an open question first: “What worked for you, and what would you change?” If using a rating, record the question, scale anchors, timing, respondent count, non-response and context. A locally drafted item is not a validated questionnaire. Pilot wording accessibly. Separate satisfaction with the result, the process and the recovery.

## Evidence record template

Use one record for a task and condition; use separate linked records where evidence differs.

- Record ID, date, service/version, task and intended end state.
- Conditions: route, chosen technology/settings, relevant interruptions and support availability.
- Linked SX categories, relevant CP identifiers and separately verified accessibility requirements.
- Observation: what happened, including errors, non-entry, abandonment and chosen or forced help.
- Participant account: their words or a consented summary, clearly separated from researcher inference.
- Functional finding, experience finding and emotional/brand finding, each with evidence or “not assessed”.
- Missing evidence, uncertainty, proposed change, responsible owner to be confirmed and retest plan.

Use `not assessed`, `evidence incomplete`, `barrier observed` and `outcome observed in stated conditions` for experience records. These are not legal conformance statuses. The repository supplies no real participant findings.

## Alignment with existing outcome guidance

The [EAA customer-outcomes guide](https://github.com/Double-FW/European-Accessibility-Act-EAA-Compliance-Approach/blob/main/guides/04-customer-outcomes-and-research.md) separately addresses accurate completion (IDSO09), effort/time (IDSO10), recovery (IDSO11), autonomy (IDSO12), continuity (IDSO15), confidence/control (IDSO16), dignity (IDSO17) and satisfaction (IDSO18). Use those existing identities when combining evidence. SX categories are a local organising aid with many-to-many relationships, not replacements or statutory tests.

Resolve a blocked or harmful task even if satisfaction is high. Investigate dissatisfaction even if technical checks pass. Link service repair and retesting to the [complaints and improvement process](Complaints_Recovery_and_Continuous_Improvement.md).
