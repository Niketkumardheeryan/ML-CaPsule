import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "check_notebooks.py"
SPEC = importlib.util.spec_from_file_location("check_notebooks", SCRIPT_PATH)
check_notebooks = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_notebooks)


def notebook(cells, **extra):
    """Build a minimal but valid notebook payload."""
    payload = {"cells": cells, "metadata": {}, "nbformat": 4, "nbformat_minor": 5}
    payload.update(extra)
    return payload


def code_cell(source="print('hi')", outputs=None):
    return {
        "cell_type": "code",
        "source": source if isinstance(source, list) else [source],
        "outputs": outputs or [],
        "execution_count": 1,
        "metadata": {},
    }


def write(payload, directory, name="demo.ipynb"):
    path = Path(directory) / name
    if isinstance(payload, str):
        path.write_text(payload, encoding="utf-8")
    else:
        path.write_text(json.dumps(payload), encoding="utf-8")
    return path


class CleanNotebookTests(unittest.TestCase):
    def test_a_healthy_notebook_reports_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = write(notebook([code_cell()]), directory)
            errors, warnings = check_notebooks.check_notebook(path)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])


class ErrorTests(unittest.TestCase):
    def test_invalid_json_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = write("{not json at all", directory)
            errors, _ = check_notebooks.check_notebook(path)
            self.assertEqual(len(errors), 1)
            self.assertIn("not valid notebook JSON", errors[0])

    def test_missing_cells_list_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = write({"metadata": {}, "nbformat": 4}, directory)
            errors, _ = check_notebooks.check_notebook(path)
            self.assertIn("no 'cells' list", errors[0])

    def test_empty_notebook_is_an_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = write(notebook([]), directory)
            errors, _ = check_notebooks.check_notebook(path)
            self.assertIn("contains no cells", errors[0])

    def test_committed_traceback_is_an_error(self):
        error_output = {
            "output_type": "error",
            "ename": "ValueError",
            "evalue": "bad input",
            "traceback": ["Traceback..."],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = write(notebook([code_cell(outputs=[error_output])]), directory)
            errors, _ = check_notebooks.check_notebook(path)
            self.assertEqual(len(errors), 1)
            self.assertIn("ValueError", errors[0])
            self.assertIn("cell 1", errors[0])

    def test_a_normal_stream_output_is_not_an_error(self):
        stream = {"output_type": "stream", "name": "stdout", "text": ["hi\n"]}
        with tempfile.TemporaryDirectory() as directory:
            path = write(notebook([code_cell(outputs=[stream])]), directory)
            errors, _ = check_notebooks.check_notebook(path)
            self.assertEqual(errors, [])


class WarningTests(unittest.TestCase):
    def test_local_mac_path_is_flagged(self):
        cell = code_cell("data = open('/Users/someone/data/train.csv')")
        with tempfile.TemporaryDirectory() as directory:
            path = write(notebook([cell]), directory)
            _, warnings = check_notebooks.check_notebook(path)
            self.assertEqual(len(warnings), 1)
            self.assertIn("local path", warnings[0])

    def test_local_linux_and_windows_paths_are_flagged(self):
        cells = [
            code_cell("p = '/home/anna/datasets/x.csv'"),
            code_cell("p = r'C:\\Users\\Anna\\data.csv'"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = write(notebook(cells), directory)
            _, warnings = check_notebooks.check_notebook(path)
            self.assertEqual(len(warnings), 2)

    def test_ci_and_colab_paths_are_allowed(self):
        cells = [
            code_cell("p = '/home/user/app/data.csv'"),
            code_cell("p = '/Users/runner/work/repo/file.csv'"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = write(notebook(cells), directory)
            _, warnings = check_notebooks.check_notebook(path)
            self.assertEqual(warnings, [])

    def test_notebook_without_code_cells_is_flagged(self):
        markdown = {"cell_type": "markdown", "source": ["# Title"], "metadata": {}}
        with tempfile.TemporaryDirectory() as directory:
            path = write(notebook([markdown]), directory)
            _, warnings = check_notebooks.check_notebook(path)
            self.assertIn("no code cells", warnings[0])

    def test_string_source_is_handled(self):
        cell = {"cell_type": "code", "source": "x = 1", "outputs": [], "metadata": {}}
        with tempfile.TemporaryDirectory() as directory:
            path = write(notebook([cell]), directory)
            errors, warnings = check_notebooks.check_notebook(path)
            self.assertEqual((errors, warnings), ([], []))


class DiscoveryTests(unittest.TestCase):
    def test_changed_files_filter_to_notebooks(self):
        with tempfile.TemporaryDirectory() as directory:
            write(notebook([code_cell()]), directory, "a.ipynb")
            Path(directory, "script.py").write_text("x = 1", encoding="utf-8")
            found = check_notebooks.find_notebooks(
                directory, ["a.ipynb", "script.py", "missing.ipynb"]
            )
            self.assertEqual([p.name for p in found], ["a.ipynb"])

    def test_checkpoints_are_ignored_in_a_full_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            write(notebook([code_cell()]), directory, "real.ipynb")
            checkpoints = Path(directory, ".ipynb_checkpoints")
            checkpoints.mkdir()
            write(notebook([code_cell()]), checkpoints, "real-checkpoint.ipynb")
            found = check_notebooks.find_notebooks(directory)
            self.assertEqual([p.name for p in found], ["real.ipynb"])

    def test_whitespace_separated_paths_are_split(self):
        self.assertEqual(
            check_notebooks.normalize_changed_files(["a.ipynb b.ipynb\nc.ipynb"]),
            ["a.ipynb", "b.ipynb", "c.ipynb"],
        )


class ReportTests(unittest.TestCase):
    def test_report_counts_errors_and_warnings(self):
        report = check_notebooks.build_report(
            [{"path": "a.ipynb", "errors": ["a.ipynb: boom"], "warnings": ["a.ipynb: hmm"]}]
        )
        self.assertIn("**Errors:** 1", report)
        self.assertIn("a.ipynb: boom", report)
        self.assertIn("a.ipynb: hmm", report)

    def test_report_with_no_notebooks(self):
        self.assertIn("No notebooks were changed", check_notebooks.build_report([]))

    def test_clean_report_says_so(self):
        report = check_notebooks.build_report(
            [{"path": "a.ipynb", "errors": [], "warnings": []}]
        )
        self.assertIn("look clean", report)


class ExitCodeTests(unittest.TestCase):
    def test_errors_exit_non_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            write("{broken", directory, "bad.ipynb")
            self.assertEqual(check_notebooks.main(["--root-dir", directory]), 1)

    def test_clean_run_exits_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            write(notebook([code_cell()]), directory, "ok.ipynb")
            self.assertEqual(check_notebooks.main(["--root-dir", directory]), 0)

    def test_warnings_alone_do_not_fail(self):
        markdown = {"cell_type": "markdown", "source": ["# Title"], "metadata": {}}
        with tempfile.TemporaryDirectory() as directory:
            write(notebook([markdown]), directory, "docs.ipynb")
            self.assertEqual(check_notebooks.main(["--root-dir", directory]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
