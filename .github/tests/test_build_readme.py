import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import build_readme


class BuildReadmeTests(unittest.TestCase):
    def test_metadata_for_beginner_and_advanced_projects(self):
        projects = [
            {"fname": "Basics of the Python", "furl": "Basics%20of%20the%20Python"},
            {"fname": "Alzheimer's Disease Predictor", "furl": "Alzheimer's%20Disease%20Predictor"},
            {"fname": "Generating 3D Design Voxels using GANs", "furl": "Generating%203D%20Design%20Voxels%20using%20GANs"},
        ]

        table = build_readme.build_project_table(projects)

        self.assertIn("Basics of the Python", table)
        self.assertIn("🟢 Beginner", table)
        self.assertIn("1-3 hours", table)
        self.assertIn("🟡 Intermediate", table)
        self.assertIn("🟠 Advanced", table)
        self.assertIn("6-12 hours", table)


if __name__ == "__main__":
    unittest.main()
