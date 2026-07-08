import json, pathlib, unittest, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestTaxonomy(unittest.TestCase):
    def setUp(self):
        self.tax = json.loads((ROOT / "taxonomy" / "domains.json").read_text(encoding="utf-8"))
        self.schema = json.loads((ROOT / "schemas" / "verdict.schema.json").read_text(encoding="utf-8"))

    def test_verdict_classes_are_the_four(self):
        self.assertEqual(set(self.tax["verdict_classes"]), {"pass", "fail", "refuse", "malformed"})

    def test_every_status_maps_to_a_valid_class(self):
        classes = set(self.tax["verdict_classes"])
        for dom in self.tax["domains"]:
            for ct in dom["claim_types"]:
                for status, cls in ct["statuses"].items():
                    self.assertIn(cls, classes, f"{dom['domain']}/{ct['type']}/{status}")

    def test_every_domain_names_a_gate(self):
        for dom in self.tax["domains"]:
            self.assertTrue(dom.get("gate"), dom["domain"])

    def test_lite_repo_urls_are_github(self):
        for dom in self.tax["domains"]:
            url = dom.get("lite_repo")
            if url:
                p = urllib.parse.urlparse(url)
                self.assertEqual(p.netloc, "github.com", url)

    def test_schema_declares_required_core_fields(self):
        self.assertEqual(set(self.schema["required"]), {"tool", "status", "passed"})

    def test_client_imports(self):
        import sys
        sys.path.insert(0, str(ROOT / "client"))
        import dtl_client
        c = dtl_client.DTLClient(api_key="test")
        self.assertTrue(c.base_url.startswith("https://"))


if __name__ == "__main__":
    unittest.main()
