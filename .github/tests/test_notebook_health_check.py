import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "notebook_health_check.py"
SPEC = importlib.util.spec_from_file_location("notebook_health_check", SCRIPT_PATH)
notebook_health_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(notebook_health_check)


class NotebookHealthCheckTests(unittest.TestCase):
    def test_marks_manual_inspection_notebooks(self):
        payload = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": [
                        "import requests\n",
                        "response = requests.get('https://example.com')\n",
                    ],
                }
            ]
        }
        notebook_path = Path("manual_review.ipynb")

        result = notebook_health_check.classify_notebook(payload, notebook_path)

        self.assertTrue(result["requires_manual_inspection"])
        self.assertFalse(result["should_run"])
        self.assertIn("manual inspection", result["reason"])

    def test_allows_simple_notebooks_to_run(self):
        payload = {
            "cells": [
                {
                    "cell_type": "code",
                    "source": [
                        "import pandas as pd\n",
                        "data = pd.DataFrame({'a': [1, 2]})\n",
                    ],
                }
            ]
        }
        notebook_path = Path("simple_notebook.ipynb")

        result = notebook_health_check.classify_notebook(payload, notebook_path)

        self.assertFalse(result["requires_manual_inspection"])
        self.assertTrue(result["should_run"])


if __name__ == "__main__":
    unittest.main()
