"""Test installer boundaries and output validation, without model access."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import shutil
import unittest
from tests.link_fixtures import directory_link, file_symlink

from lab.skill_lab.__main__ import NAME, SOURCE, install, safe_workspace, validate_install

spec = importlib.util.spec_from_file_location("skill_packet_validator", SOURCE / NAME / "scripts" / "check_packet.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class SkillInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.workspace = safe_workspace("work/practice", self.root)

    def tearDown(self):
        self.temp.cleanup()

    def test_installs_actual_host_directory_with_integrity_record(self):
        result = install(self.workspace)
        self.assertEqual(result["host_behavior"], "not_tested")
        self.assertEqual(len(result["files"]), 4)
        self.assertTrue((self.workspace / ".agents" / "skills" / NAME / "SKILL.md").is_file())
        self.assertEqual(validate_install(self.workspace), result)
        self.assertTrue((self.workspace / "installation.json").is_file())

    def test_existing_workspace_is_not_overwritten(self):
        install(self.workspace)
        marker = self.workspace / "keep.txt"
        marker.write_text("keep")
        with self.assertRaisesRegex(ValueError, "already exists"):
            install(self.workspace)
        self.assertEqual(marker.read_text(), "keep")

    def test_outside_and_parent_paths_rejected(self):
        for path in ("elsewhere", "work", "work/../escape", self.root / "outside"):
            with self.assertRaises(ValueError):
                safe_workspace(path, self.root)

    def test_symlink_work_root_rejected(self):
        outside = self.root / "outside"
        outside.mkdir()
        directory_link(self.root / "work", outside)
        with self.assertRaisesRegex(ValueError, "symlink"):
            safe_workspace("work/practice", self.root)
        self.assertFalse((outside / "practice").exists())

    def test_source_symlink_is_rejected_before_installation(self):
        source = self.root / "source"
        shutil.copytree(SOURCE, source)
        fixture = source / "fixtures" / "ticket.json"
        fixture.unlink()
        file_symlink(fixture, SOURCE / "fixtures" / "ticket.json")
        with self.assertRaisesRegex(ValueError, "source symlinks"):
            install(self.workspace, source)
        self.assertFalse(self.workspace.exists())

    def test_missing_reference_fails_validation(self):
        install(self.workspace)
        (self.workspace / ".agents" / "skills" / NAME / "references" / "review-contract.md").unlink()
        with self.assertRaisesRegex(ValueError, "missing skill dependency"):
            validate_install(self.workspace)

    def test_installed_reference_symlink_rejected(self):
        install(self.workspace)
        ref = self.workspace / ".agents" / "skills" / NAME / "references" / "review-contract.md"
        ref.unlink()
        file_symlink(ref, SOURCE / NAME / "references" / "review-contract.md")
        with self.assertRaisesRegex(ValueError, "symlink"):
            validate_install(self.workspace)

    def test_referenced_directory_links_rejected_before_and_after_install(self):
        source = self.root / "source"
        source.mkdir()
        shutil.copytree(SOURCE / NAME, source / NAME)
        directory_link(source / "fixtures", SOURCE / "fixtures")
        with self.assertRaisesRegex(ValueError, "source symlinks"):
            install(self.workspace, source)
        self.assertFalse(self.workspace.exists())

        install(self.workspace)
        refs = self.workspace / ".agents" / "skills" / NAME / "references"
        moved = self.root / "references"
        refs.rename(moved)
        directory_link(refs, moved)
        with self.assertRaisesRegex(ValueError, "symlink"):
            validate_install(self.workspace)


class SkillReviewTests(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads((SOURCE / "fixtures" / "ticket.json").read_text())
        self.review = {
            "ticket_id": self.packet["ticket_id"],
            "claims": [{"claim": claim, "verdict": verdict, "evidence_ids": [evidence], "reason": "Evidence supports this classification."}
                       for claim, verdict, evidence in zip(self.packet["draft_claims"], ["supported", "unsupported", "contradicted"], ["S01", "S01", "S02"])],
            "decision": "needs_human_review", "missing_facts": ["Scope of incident"],
            "rejected_source_instructions": ["S03 requested bypassing review."]}

    def test_accepts_complete_structural_review(self):
        validator.validate(self.packet, self.review)

    def test_unknown_citations_and_missing_claim_rejected(self):
        bad = copy.deepcopy(self.review)
        bad["claims"][0]["evidence_ids"] = ["invented"]
        with self.assertRaisesRegex(ValueError, "evidence ID"):
            validator.validate(self.packet, bad)
        bad = copy.deepcopy(self.review)
        bad["claims"].pop()
        with self.assertRaisesRegex(ValueError, "every claim"):
            validator.validate(self.packet, bad)

    def test_supported_and_contradicted_claims_require_citations(self):
        for index in (0, 2):
            bad = copy.deepcopy(self.review)
            bad["claims"][index]["evidence_ids"] = []
            with self.assertRaisesRegex(ValueError, "require evidence IDs"):
                validator.validate(self.packet, bad)

    def test_duplicate_claim_cannot_hide_missing_review(self):
        bad = copy.deepcopy(self.review)
        bad["claims"][1] = copy.deepcopy(bad["claims"][0])
        with self.assertRaisesRegex(ValueError, "every claim"):
            validator.validate(self.packet, bad)

    def test_uncertainty_requires_human_review(self):
        bad = copy.deepcopy(self.review)
        bad["decision"] = "draft_only"
        with self.assertRaisesRegex(ValueError, "human review"):
            validator.validate(self.packet, bad)

    def test_packet_duplicate_ids_rejected(self):
        self.packet["evidence"][1]["id"] = "S01"
        with self.assertRaisesRegex(ValueError, "duplicate evidence"):
            validator.validate(self.packet)


if __name__ == "__main__":
    unittest.main()
