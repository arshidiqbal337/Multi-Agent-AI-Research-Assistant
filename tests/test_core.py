"""Unit tests for the offline research-agent pipeline."""

import unittest

from agents.core import SearchAgent, SummaryAgent, VerificationAgent, run_pipeline


class TestResearchAgents(unittest.TestCase):
    def setUp(self):
        self.documents = {
            "sample.txt": (
                "Retrieval augmented generation uses relevant documents to support generated answers. "
                "Evidence verification helps readers inspect source passages in research reports."
            )
        }

    def test_search_finds_relevant_passage(self):
        results = SearchAgent().run("What is retrieval augmented generation?", self.documents)
        self.assertTrue(results)
        self.assertEqual(results[0]["source"], "sample.txt")

    def test_summary_includes_source(self):
        evidence = SearchAgent().run("retrieval augmented generation", self.documents)
        summary = SummaryAgent().run(evidence)
        self.assertIn("sample.txt", summary)

    def test_verification_with_no_evidence(self):
        result = VerificationAgent().run([])
        self.assertEqual(result["status"], "Insufficient evidence")

    def test_pipeline_returns_report(self):
        result = run_pipeline("retrieval augmented generation", self.documents)
        self.assertIn("report", result)
        self.assertIn("summary", result)
        self.assertIn("evidence", result)
        self.assertIn("Research report", result["report"])


if __name__ == "__main__":
    unittest.main()
