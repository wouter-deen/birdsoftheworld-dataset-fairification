import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from subprocess import run

from extract_description_features import categorical_values, extract


class DescriptionFeatureTests(unittest.TestCase):
    def test_body_part_colors_are_separate(self):
        self.assertEqual(
            extract("A large bird with a white head and brown body"),
            {"size_large", "color_head_white", "color_body_brown"},
        )

    def test_hyphenated_plumage_and_unspecified_are_not_confused(self):
        features = extract(
            "A small warbler with black-and-white plumage and a red bill"
        )
        self.assertTrue(
            {"color_plumage_black", "color_plumage_white", "color_bill_red"} <= features
        )
        self.assertNotIn("color_plumage_red", features)
        self.assertNotIn("color_bill_black", features)

    def test_color_list_and_normalization(self):
        self.assertTrue(
            {"color_plumage_green", "color_plumage_brown", "color_plumage_white"}
            <= extract(
                "A duck with colorful plumage, including green, brown, and white"
            )
        )
        self.assertIn(
            "color_back_gray_brown", extract("A bird with a grayish-brown back")
        )
        self.assertNotIn("color_back_gray", extract("A bird with a grayish-brown back"))

    def test_anatomy_vocalization_and_no_habitat_inference(self):
        features = extract(
            "A small owl with ear tufts, a hooked beak, and a hooting call"
        )
        self.assertTrue(
            {"size_small", "head_ear_tufts", "bill_shape_hooked", "vocalization_call"}
            <= features
        )
        self.assertFalse(any(f.startswith("habitat_") for f in features))

    def test_variations(self):
        self.assertIn(
            "color_plumage_red", extract("A bird with bright scarlet plumage")
        )
        self.assertIn("color_plumage_brown", extract("A bird with brownish-plumage"))
        self.assertIn("color_tail_yellow", extract("A bird with a yellow-tipped tail"))
        self.assertIn("bill_shape_curved", extract("A bird with a long curved bill"))
        self.assertNotIn(
            "bill_shape_downcurved", extract("A bird with a long curved bill")
        )
        self.assertIn(
            "bill_shape_downcurved", extract("A bird with a downward-curved bill")
        )

    def test_multiple_values_share_a_column(self):
        values = categorical_values(
            extract(
                "A small bird with black-and-white plumage, a white head, and a hooked bill"
            )
        )
        self.assertEqual(values["size"], "small")
        self.assertEqual(values["plumage_color"], "black|white")
        self.assertEqual(values["head_color"], "white")
        self.assertEqual(values["bill_shape"], "hooked")
        self.assertNotIn("color_plumage_black", values)

    def test_pipeline_defaults_write_to_outputs_from_another_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            for script in ("preprocessing.py", "extract_description_features.py"):
                shutil.copyfile(
                    Path(__file__).resolve().parent / script, project / script
                )
            (project / "Birdsoftheworld.csv").write_text(
                "species,location,time,description of bird,sex,feather color\n"
                "American Robin,New York City,15-06-2023 08:30,"
                "A small bird with an orange breast,Unknown,Brown\n",
                encoding="utf-8",
            )
            elsewhere = project / "elsewhere"
            elsewhere.mkdir()
            for args in (
                ("preprocessing.py",),
                ("extract_description_features.py", "--report"),
            ):
                result = run(
                    [sys.executable, str(project / args[0]), *args[1:]],
                    cwd=elsewhere,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(
                (project / "outputs" / "Birdsoftheworld-preprocessed.csv").exists()
            )
            self.assertTrue(
                (project / "outputs" / "Birdsoftheworld-features.csv").exists()
            )
            self.assertTrue(
                (project / "outputs" / "description-feature-analysis.md").exists()
            )
            self.assertFalse((project / "Birdsoftheworld-features.csv").exists())
            self.assertFalse((project / "Birdsoftheworld-preprocessed.csv").exists())
            with (project / "outputs" / "Birdsoftheworld-features.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
                self.assertEqual(next(csv.DictReader(handle))["size"], "small")

    def test_csv_preserves_rows_and_unknowns(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            output = Path(directory) / "output.csv"
            report = Path(directory) / "report.md"
            with source.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(["species", "description of bird", "feather color"])
                writer.writerow(["Owl", "A large white owl with ear tufts", "White"])
                writer.writerow(["Finch", "A small finch with a red bill", "Yellow"])
            result = run(
                [
                    sys.executable,
                    "extract_description_features.py",
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                    "--report",
                    str(report),
                ],
                cwd=Path(__file__).resolve().parent,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["feather color"], "White")
            self.assertEqual(rows[0]["size"], "large")
            self.assertEqual(rows[0]["plumage_color"], "white")
            self.assertEqual(rows[0]["head_ornament"], "ear_tufts")
            self.assertEqual(rows[1]["plumage_color"], "")
            self.assertEqual(rows[1]["bill_color"], "red")
            self.assertNotIn("color_bill_red", rows[1])
            self.assertIn(
                "| `bill_color` | `red` | 1 | 50.0% | 1 |", report.read_text()
            )


if __name__ == "__main__":
    unittest.main()
