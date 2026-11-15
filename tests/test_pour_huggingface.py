"""Faithful export and guarded publication tests with no live dataset writes."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import pour_hf_common as common
import export_huggingface as exporter
import publish_huggingface as publisher

class POURSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.repo = self.base/'repo'
        self.repo.mkdir()
        cfg = common.load_config(ROOT)
        for name in cfg['files'] + ['LICENSE']:
            result = subprocess.run(['git', '-C', str(ROOT), 'show', 'HEAD:' + name], capture_output=True)
            if result.returncode:
                if name in cfg['required_files']: self.fail('Required source absent: ' + name)
                continue
            (self.repo/name).write_bytes(result.stdout)
        shutil.copytree(ROOT/'huggingface', self.repo/'huggingface')
        self.git('init', '-q'); self.git('config', 'user.name', 'Test fixture')
        self.git('config', 'user.email', 'test@example.invalid'); self.commit()
        self.out = self.base/'export'
    def git(self, *args): return common.git(self.repo, *args)
    def commit(self):
        self.git('add', '.'); self.git('commit', '--allow-empty', '-qm', 'Fixture')
    def build(self): return exporter.build(self.repo, self.out)
    def rows(self, name): return [json.loads(x) for x in (self.out/name).read_text().splitlines()]

    def test_documents_and_sections_reproduce_exact_source_bytes(self):
        self.build()
        for row in self.rows('documents.jsonl'):
            self.assertEqual(row['text'].encode(), self.git('show', 'HEAD:' + row['source_path']))
            joined = ''.join(x['text'] for x in self.rows('knowledge_chunks.jsonl') if x['source_path'] == row['source_path'])
            self.assertEqual(joined, '' if row['source_path']==exporter.POLICY else row['text'])

    def test_metadata_licence_warnings_and_status_remain_visible(self):
        report = self.build()
        agent = next(x for x in self.rows('documents.jsonl') if x['source_path'] == 'AGENTS.md')
        original = exporter.metadata(self.git('show', 'HEAD:AGENTS.md').decode())
        self.assertEqual(agent['declared_source_license'], str(original.get('license', 'not_declared_in_document_front_matter')))
        self.assertEqual(agent['source_status'], str(original.get('status', 'see_source')))
        if original.get('license') == 'NOASSERTION':
            self.assertTrue(any('NOASSERTION' in w for w in report['source_warnings']))
        self.assertEqual((self.out/'LICENSE').read_bytes(), self.git('show', 'HEAD:LICENSE'))

    def test_headings_fences_and_parent_context(self):
        text = '---\nstatus: draft\n---\n# Parent\n## One\n```md\n## Example only\n```\n# Second parent\n## Two\nBody\n'
        parts = exporter.sections(text)
        self.assertEqual(''.join(x[2] for x in parts), text)
        self.assertEqual(len(parts), 5)
        self.assertEqual(parts[-1][-1], ['Second parent', 'Two'])
        self.assertIn('Example only', parts[2][2])

    def test_output_is_repeatable(self):
        self.build(); before = {p.name:p.read_bytes() for p in self.out.iterdir()}
        self.build(); self.assertEqual(before, {p.name:p.read_bytes() for p in self.out.iterdir()})

    def test_new_unapproved_and_untracked_material_stays_out(self):
        (self.repo/'not-approved.md').write_text('Not approved'); self.commit()
        (self.repo/'private-notes.md').write_text('Untracked private')
        self.build()
        data = (self.out/'documents.jsonl').read_text()
        self.assertNotIn('not-approved.md', data); self.assertNotIn('Untracked private', data)

    def test_missing_policy_source_blocks_export(self):
        (self.repo/exporter.POLICY).unlink();self.commit()
        with self.assertRaises(ValueError):self.build()

    def test_policy_proposals_are_complete_and_unexecuted(self):
        self.build();rows=self.rows('documents.jsonl')
        policy=next(r for r in rows if r['source_path']==exporter.POLICY)
        original=exporter.safe_yaml(self.git('show','HEAD:'+exporter.POLICY).decode())
        self.assertEqual(json.loads(policy['structured_policy_proposals_json']),original)
        self.assertEqual(policy['source_policy_ids'],[r['id'] for r in original['policies']])
        self.assertIn('proposed',policy['record_type'])
        self.assertFalse(any(r['source_path']==exporter.POLICY for r in self.rows('knowledge_chunks.jsonl')))
        p=json.loads((self.out/'provenance.json').read_text())
        for k in ['policy_actions_executed','customer_outcomes_verified','governance_services_configured']:self.assertFalse(p[k])

    def test_fifth_principle_remains_a_proposal(self):
        self.build();rows=self.rows('knowledge_chunks.jsonl')
        row=next(r for r in rows if r['record_type']=='proposed_fifth_emotional_principle_not_wcag')
        self.assertIn('Satisfactory',row['text'])
        self.assertIn('not WCAG amendments',row['interpretation_notice'])
        self.assertIn(exporter.ARTICLE,row['required_context_paths'])

    def test_duplicate_policy_ids_keys_and_unsafe_yaml_reject(self):
        import yaml
        p=self.repo/exporter.POLICY;d=exporter.safe_yaml(p.read_text());d['policies'].append(d['policies'][0]);p.write_text(yaml.safe_dump(d));self.commit()
        with self.assertRaises(ValueError):self.build()
        with self.assertRaises(ValueError):exporter.safe_yaml('a: 1\na: 2\n')
        with self.assertRaises(yaml.constructor.ConstructorError):exporter.safe_yaml('!!python/object/apply:os.system [echo forbidden]')

    def test_tokens_with_linebreaks_reject_without_network(self):
        self.build()
        with self.assertRaises(ValueError):publisher.publish(self.out,'fake-token\n',check_public=lambda:self.fail('No network expected'))

    def test_missing_required_and_changed_licence_block(self):
        (self.repo/'AGENTS.md').unlink(); self.commit()
        with self.assertRaises(ValueError): self.build()
        self.git('reset', '--hard', 'HEAD~1')
        (self.repo/'LICENSE').write_text('Unapproved new terms'); self.commit()
        with self.assertRaises(ValueError): self.build()

    def test_wrong_source_or_destination_and_output_location_block(self):
        for target in ('', 'GarethFW/accessible-chatbots', 'GarethFW/AVMSD_delivery_and_evidence_repository'):
            with self.assertRaises(ValueError): common.destination(target)
        cfg_path = self.repo/'huggingface/export-config.json'
        cfg = json.loads(cfg_path.read_text()); cfg['source_repository'] = 'Someone/Else'; cfg_path.write_text(json.dumps(cfg))
        with self.assertRaises(ValueError): self.build()
        with self.assertRaises(ValueError): exporter.build(self.repo, self.repo/'export')

    def test_private_source_blocked(self):
        response = Mock(); response.read.return_value = json.dumps({'full_name':common.SOURCE, 'private':True, 'visibility':'private'}).encode()
        response.__enter__ = Mock(return_value=response); response.__exit__ = Mock(return_value=False)
        with patch.object(common.urllib.request, 'urlopen', return_value=response):
            with self.assertRaises(ValueError): common.public_source()

    def test_noop_first_publish_and_destination_protection(self):
        self.build(); api=Mock(); api.repo_info.return_value.sha='read-destination-revision'
        def same(**kw): return str(self.out/kw['filename'])
        result=publisher.publish(self.out, 'fake-test-token', api=api, download=same, check_public=lambda:None)
        self.assertIn('No changes', result); api.create_commit.assert_not_called()
        from huggingface_hub.errors import EntryNotFoundError
        def empty(**kw): raise EntryNotFoundError('Missing test file')
        publisher.publish(self.out, 'fake-test-token', api=api, download=empty, check_public=lambda:None)
        args=api.create_commit.call_args.kwargs
        self.assertEqual(args['repo_id'], 'GarethFW/POUR_for_Branding_Systems_and_CX')
        self.assertEqual(args['parent_commit'], 'read-destination-revision')
        self.assertEqual({x.path_in_repo for x in args['operations']}, set(common.MANAGED))
        self.assertNotIn('.gitattributes', {x.path_in_repo for x in args['operations']})
        api.create_repo.assert_not_called(); api.update_repo_settings.assert_not_called()

    def test_missing_token_tampering_and_foreign_provenance_block(self):
        self.build(); api=Mock(); api.repo_info.return_value.sha='head'
        with self.assertRaises(ValueError): publisher.publish(self.out, '', check_public=lambda:None)
        foreign=self.base/'foreign.json'; foreign.write_text(json.dumps({'source_repository':'Another/Source'}))
        def wrong(**kw): return str(foreign if kw['filename']=='provenance.json' else self.out/kw['filename'])
        with self.assertRaises(ValueError): publisher.publish(self.out, 'fake', api=api, download=wrong, check_public=lambda:None)
        (self.out/'README.md').write_text('Tampered export')
        with self.assertRaises(ValueError): publisher.publish(self.out, 'fake', api=api, download=wrong, check_public=lambda:None)

    def test_change_report_distinguishes_removals_and_revision_only_changes(self):
        delta=publisher.changes_between([{'id':'removed','text':'x'}, {'id':'same','text':'x','source_commit':'old'}],
                                        [{'id':'added','text':'y'}, {'id':'same','text':'x','source_commit':'new'}])
        self.assertEqual(delta, {'added':['added'], 'removed':['removed'], 'updated':[]})

    def test_workflow_matches_this_repository_and_preset_destination(self):
        import yaml
        workflow=yaml.load((ROOT/'.github/workflows/huggingface-sync.yml').read_text(), Loader=yaml.BaseLoader)
        self.assertIn("github.repository == 'Double-FW/POUR-for-Branding-Systems-and-CX'", workflow['jobs']['publish']['if'])
        self.assertIn('workflow_dispatch', workflow['on'])
        self.assertEqual(common.load_config(ROOT)['destination_dataset'], 'GarethFW/POUR_for_Branding_Systems_and_CX')

if __name__ == '__main__': unittest.main()
