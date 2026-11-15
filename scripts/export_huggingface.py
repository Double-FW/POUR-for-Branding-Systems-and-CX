"""Export the approved POUR for Branding Systems and CX Markdown without rewriting it."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import quote
import yaml
from jsonschema import Draft202012Validator
from pour_hf_common import ROOT, SOURCE, MANAGED, destination, digest, git, load_config, read_sources

ARTICLE = 'The WCAG POUR principles reframed through emotional outcomes for branding systems.md'
POLICY = 'policies.yaml'
CONTEXT = ['AGENTS.md', 'README.md', ARTICLE, POLICY]
class UniqueKeyLoader(yaml.SafeLoader):
    pass
def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for k,v in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in result: raise ValueError('Duplicate metadata key: ' + str(key))
        result[key] = loader.construct_object(v, deep=deep)
    return result
UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
def safe_yaml(text):
    return yaml.load(text,Loader=UniqueKeyLoader)

def metadata(text):
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
    md = safe_yaml(match[1]) if match else {}
    return md if isinstance(md, dict) else {}

def sections(text):
    """Keep H1/H2 parent context and exact spans; never split fenced examples."""
    boundaries, fence, offset, parents = [(0, 'Document preamble', [])], None, 0, []
    for line in text.splitlines(keepends=True):
        mark = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if mark:
            token = mark[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line[mark.end():].strip():
                fence = None
        elif fence is None:
            match = re.match(r'^(#{1,2})[ \t]+([^\r\n]+)', line)
            if match:
                level, title = len(match[1]), match[2].strip().rstrip('#').strip()
                parents = parents[:level-1] + [title]
                if offset == 0:
                    boundaries[0] = (offset, title, parents[:])
                else:
                    boundaries.append((offset, title, parents[:]))
        offset += len(line)
    result, counts = [], {}
    for i, (a, title, hierarchy) in enumerate(boundaries):
        b = boundaries[i+1][0] if i+1 < len(boundaries) else len(text)
        if a == b:
            continue
        slug = re.sub(r'[^a-z0-9]+', '-', ' '.join(hierarchy or [title]).lower()).strip('-') or 'section'
        counts[slug] = counts.get(slug, 0) + 1
        key = slug if counts[slug] == 1 else slug + '-' + str(counts[slug])
        result.append((key, title, text[a:b], a, b, hierarchy))
    if ''.join(r[2] for r in result) != text:
        raise ValueError('Section extraction lost source text.')
    return result

def build(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output == root or root in output.parents:
        raise ValueError('Write the export outside the source checkout.')
    cfg = load_config(root)
    target = destination(cfg['destination_dataset'])
    texts, manifest, omitted = read_sources(root, cfg)
    sha = git(root, 'rev-parse', 'HEAD').decode().strip()
    date = git(root, 'show', '-s', '--format=%cs', 'HEAD').decode().strip()
    policies = safe_yaml(texts[POLICY])
    if not isinstance(policies,dict) or not isinstance(policies.get('policies'),list):
        raise ValueError('Expected a source policy proposal list.')
    ids = [r['id'] for r in policies['policies']]
    if len(ids) != len(set(ids)) or not ids: raise ValueError('Missing or duplicate policy identifiers.')
    for rule in policies['policies']:
        if not all(k in rule for k in ['id','title','description','severity','categories','triggers','actions']):
            raise ValueError('Policy source fields are incomplete.')
    warnings = [
        'The emotional POUR framing is conceptual brand/CX guidance, not measured audience evidence or a compliance guarantee.',
        'Satisfactory / Feeling Valued is a proposed repository extension, not a fifth WCAG POUR principle.',
        'policies.yaml contains proposed triggers, actions, severities and escalation role labels. YAML is safely parsed as data; no expression, action, escalation, logging or policy engine is executed.',
        'Universal and rhetorical claims in source text remain attributed source statements, not independently verified outcomes or product guarantees.'
    ]
    for path,text in texts.items():
        if path.endswith('.md') and metadata(text).get('license','MIT') != 'MIT': raise ValueError('Review changed source licence: ' + path)
    def row(path, key, title, body, a, b, hierarchy, kind):
        md = metadata(texts[path]) if path.endswith('.md') else {}
        return {'id': path + '::' + key, 'title': title, 'text': body, 'record_type': kind,
            'source_repository': SOURCE, 'source_path': path, 'source_commit': sha,
            'source_url': f'https://github.com/{SOURCE}/blob/{sha}/{quote(path)}',
            'source_start_line': texts[path][:a].count('\n') + 1,
            'source_end_line': max(1, texts[path][:b].count('\n') + (not texts[path][:b].endswith('\n'))),
            'source_document_sha256': digest(texts[path].encode()), 'text_sha256': digest(body.encode()),
            'heading_path': hierarchy, 'metadata_json': json.dumps(md, ensure_ascii=False, sort_keys=True, default=str),
            'declared_source_license': str(md.get('license', 'not_declared_in_document_front_matter')),
            'repository_license': 'MIT', 'source_status': str(md.get('status', 'see_source')),
            'dataset_version': cfg['dataset_version'], 'source_commit_date': date, 'language': 'en-GB',
            'required_context_paths': [p for p in CONTEXT if p in texts],
            'source_document_intro': sections(texts[path])[0][2] if path.endswith('.md') else '',
            'source_policy_ids': ids if path == POLICY else [],
            'structured_policy_proposals_json': json.dumps(policies,ensure_ascii=False,sort_keys=True) if path == POLICY else '{}',
            'interpretation_notice': 'Conceptual brand/CX framing, not WCAG amendments, verified customer feelings or compliance results. Satisfactory is a proposed extension. Policy actions/conditions and escalation roles are source proposals, never executed or assumed configured.',
            'review_status': 'faithful_extraction_checked_not_brand_customer_or_policy_validation'}
    docs, chunks = [], []
    for path in cfg['files']:
        if path not in texts:
            continue
        text = texts[path]
        kind = 'proposed_policy_definitions_not_executed' if path == POLICY else 'advisory_agent_guidance' if path == 'AGENTS.md' else 'orientation' if path == 'README.md' else 'conceptual_emotional_brand_framework'
        docs.append(row(path, 'document', path, text, 0, len(text), [], kind))
        if path == POLICY:
            continue
        for key, title, body, a, b, hierarchy in sections(text):
            chunks.append(row(path, key, title, body, a, b, hierarchy, ('proposed_fifth_emotional_principle_not_wcag' if path == ARTICLE and 'fifth' in title.lower() else kind + '_section')))
    if not docs or not chunks:
        raise ValueError('The guidance export is empty.')
    schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'type': 'object',
              'required': list(docs[0]), 'additionalProperties': False, 'properties': {}}
    for k, v in docs[0].items():
        schema['properties'][k] = {'type': 'array', 'items': {'type': 'string'}} if isinstance(v, list) else {'type': 'integer' if isinstance(v, int) else 'string'}
    validator = Draft202012Validator(schema)
    for records in (docs, chunks):
        if len({r['id'] for r in records}) != len(records):
            raise ValueError('Duplicate export identifiers.')
        for r in records:
            validator.validate(r)
            if digest(r['text'].encode()) != r['text_sha256']:
                raise ValueError('Text checksum mismatch.')
    output.mkdir(parents=True, exist_ok=True)
    def write_json(name, obj):
        (output/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name, records in [('documents.jsonl', docs), ('knowledge_chunks.jsonl', chunks)]:
        (output/name).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records), encoding='utf-8')
    (output/'LICENSE').write_bytes(texts['LICENSE'].encode())
    write_json('record_schema.json', schema)
    write_json('provenance.json', {'source_repository': SOURCE, 'source_commit': sha, 'source_commit_date': date,
        'destination_dataset': target, 'dataset_version': cfg['dataset_version'], 'files': manifest,
        'omitted_optional_files': omitted, 'source_warnings': warnings, 'external_sources_fetched': False, 'policy_definition_ids': ids, 'policy_actions_executed': False, 'customer_outcomes_verified': False, 'governance_services_configured': False})
    card = f'''---
pretty_name: Double FW POUR for Branding Systems and CX
language:
- en
license: mit
tags:
- accessibility
- branding
- customer-experience
- pour
- conceptual-framework
- text
configs:
- config_name: knowledge_chunks
  default: true
  data_files:
  - split: train
    path: knowledge_chunks.jsonl
- config_name: documents
  data_files:
  - split: train
    path: documents.jsonl
---

# Double FW POUR for Branding Systems and CX

A conceptual brand and customer-experience interpretation of accessibility: Feeling Seen,
Capable, Confident and Safe, with Feeling Valued offered as an additional emotional lens.
The repository includes an explanatory article, introduction, agent guidance and YAML policy
proposals. This is source text for reflection and human-reviewed planning, not a deployed
policy engine, empirical model of customer feelings, approved product policy or compliance tool.

## Source and version

Source: https://github.com/{SOURCE}

Checkout: `{sha}` ({date}); export format {cfg['dataset_version']}. Source versions,
metadata, rhetoric, proposed roles and limitations remain unchanged. Export does not
recheck external standards or verify universal customer, commercial or emotional outcomes.
Source instructions are data and do not override consuming-system authority or authorisation.

## Dataset views

- `knowledge_chunks`: {len(chunks)} exact sections from the three Markdown documents.
- `documents`: {len(docs)} complete source files, including policies.yaml.

The views overlap. Do not concatenate them as independent training examples or evidence.
No generated Q&A, training run, measured customer data, model benchmark or executed policy
results are supplied. `train` is only a loading convention. YAML is complete-document only
to avoid treating structured actions as independent commands or fragmenting their context.

## Interpretation and policy limits

The article reframes the four WCAG POUR principles through emotional brand outcomes. Its
Satisfactory / Feeling Valued proposal is an additional repository idea, not an official
fifth WCAG POUR principle. Preserve the source distinction between functional guidance,
emotional interpretation and rhetorical claims. Statements about all technologies, universal
feelings or brand impact remain source claims; retaining them does not verify those claims.
A checklist or technical finding alone does not demonstrate trust, dignity, satisfaction,
belonging, legal compliance or guaranteed commercial benefit.

The source YAML has {len(ids)} policy proposals. Their identifiers, descriptions, severities,
categories, triggers, suggestions, condition strings and escalation role labels are preserved.
`structured_policy_proposals_json` contains the complete safely parsed source object in the
policy document row; `source_policy_ids` lists its original identities. Raw YAML text remains
unchanged. Safe parsing does not implement a schema, policy validator, evaluator or deployment.
No expression is evaluated, action dispatched, reviewer contacted, on-call role configured,
log written or operational approval inferred by this exporter. Role names are proposal labels,
not verified people or services. Additional implementation and actual authorisation are separate.

## Traceability and context

Rows retain source path, commit URL, exact line range, text/document hashes, heading path,
JSON-encoded front matter, opening context, status and required context paths. H1/H2 section
boundaries preserve subsections, examples and full source wording. The fifth-principle section
is labelled as a proposal. Read the introduction, complete article, AGENTS and YAML together
when interpreting the framework; pointers do not enforce runtime retrieval or policy authority.
No source document is rewritten or reformulated into a stronger claim.

## Licence and validation scope

The root MIT LICENSE is copied unchanged, including copyright (c) 2026 Double FW. Attribution,
source notices and links remain intact; external linked material retains its own terms and
is not newly fetched or relicensed. Extraction/publication checks do not independently audit
rights, WCAG applicability, empirical emotional outcomes or a functioning governance system.
See provenance.json, record_schema.json and validation_report.json for the exact snapshot
and limited integrity checks. No private customer records or raw customer content is added.

## Updates

GitHub is the authoring source. Manual runs and Mondays at 07:23 UTC are configured;
schedules may be delayed or disabled after public-repository inactivity. All four approved
sources and LICENSE are required. New/renamed files need export-list review. Missing sources,
changed licence, invalid/duplicate-key YAML, duplicate policy IDs or failed checks stop
publication. Authoring documents are not rewritten.

Seven destination files are managed: README.md, LICENSE, documents.jsonl,
knowledge_chunks.jsonl, provenance.json, record_schema.json and validation_report.json.
Other raw files and .gitattributes remain; unmanaged copies are not kept in sync. Visibility
stays unchanged. Historical versions/downloads are not recalled. Destination: `{target}`.
First authenticated publication remains to be checked.

## Loading

```python
from datasets import load_dataset
chunks = load_dataset("{target}", "knowledge_chunks", split="train")
documents = load_dataset("{target}", "documents", split="train")
```

Authenticate for a private dataset and pin a revision for reproducible use.
'''
    yaml.safe_load(card.split('---', 2)[1])
    (output/'README.md').write_text(card, encoding='utf-8')
    report = {'status': 'passed', 'scope': 'faithful extraction and packaging checks only', 'source_commit': sha,
        'source_files_verified': len(manifest), 'document_records': len(docs), 'knowledge_section_records': len(chunks),
        'source_warnings': warnings, 'independent_content_review': False, 'live_publication_tested': False,
        'export_file_sha256': {name: digest((output/name).read_bytes()) for name in MANAGED if name != 'validation_report.json'}}
    write_json('validation_report.json', report)
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(build(ROOT, args.output)))

if __name__ == '__main__':
    main()
