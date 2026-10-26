import json
import unittest
from pathlib import Path

import shortestpath


ROOT = Path(__file__).resolve().parents[1]


class ShortestPathTests(unittest.TestCase):
    def test_returns_start_when_source_is_the_target(self):
        graph = {"a": ["b"], "b": ["a"]}

        self.assertEqual(shortestpath.shortest_path(graph, "a", "a"), ["a"])

    def test_prefers_the_fewest_borders(self):
        graph = {
            "a": ["b", "c"],
            "b": ["a", "d"],
            "c": ["a", "d"],
            "d": ["b", "c", "e"],
            "e": ["d"],
        }

        self.assertEqual(
            shortestpath.shortest_path(graph, "a", "e"),
            ["a", "b", "d", "e"],
        )

    def test_returns_none_when_the_countries_are_disconnected(self):
        graph = {"a": ["b"], "b": ["a"], "c": ["d"], "d": ["c"]}

        self.assertIsNone(shortestpath.shortest_path(graph, "a", "c"))


class ValidateGraphTests(unittest.TestCase):
    def test_rejects_a_non_dictionary(self):
        self.assertEqual(
            shortestpath.validate_graph([]),
            ["Graph must be a dictionary."],
        )

    def test_rejects_duplicate_unknown_self_and_one_way_borders(self):
        graph = {
            "a": ["b", "b", "a", "missing"],
            "b": [],
            1: "nope",
        }

        errors = shortestpath.validate_graph(graph)

        self.assertIn("a: duplicate border.", errors)
        self.assertIn("a: borders itself.", errors)
        self.assertIn("a -> missing: unknown country.", errors)
        self.assertIn("a -> b: missing reverse border.", errors)
        self.assertIn("Invalid country name: 1", errors)
        self.assertIn("1: borders must be a list.", errors)

    def test_make_graph_consistent_adds_the_missing_country_and_reverse_border(self):
        graph = {"a": ["b"]}

        fixed = shortestpath.make_graph_consistent(graph)

        self.assertEqual(fixed["a"], ["b"])
        self.assertEqual(fixed["b"], ["a"])
        self.assertEqual(shortestpath.validate_graph(fixed), [])


class CountriesFileTests(unittest.TestCase):
    def setUp(self):
        with open(ROOT / "countries.json", "r") as handle:
            self.graph = json.load(handle)

    def test_checked_in_borders_are_consistent(self):
        self.assertEqual(shortestpath.validate_graph(self.graph), [])

    def test_haiti_stays_disconnected_from_the_mainland(self):
        self.assertEqual(
            shortestpath.shortest_path(self.graph, "Haiti", "Dominican Republic"),
            ["Haiti", "Dominican Republic"],
        )
        self.assertIsNone(shortestpath.shortest_path(self.graph, "Haiti", "France"))

    def test_east_timor_to_lesotho_keeps_the_published_route(self):
        self.assertEqual(
            shortestpath.shortest_path(self.graph, "East Timor", "Lesotho"),
            [
                "East Timor",
                "Indonesia",
                "Malaysia",
                "Thailand",
                "Laos",
                "China",
                "Afghanistan",
                "Iran",
                "Iraq",
                "Jordan",
                "Palestine",
                "Egypt",
                "Sudan",
                "Central African Republic",
                "Democratic Republic of the Congo",
                "Angola",
                "Namibia",
                "South Africa",
                "Lesotho",
            ],
        )


if __name__ == "__main__":
    unittest.main()
