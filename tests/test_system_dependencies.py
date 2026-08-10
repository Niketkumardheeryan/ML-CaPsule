import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

class TestSystemDependencies(unittest.TestCase):
    def test_root_requirements_exists_and_contains_tooling(self):
        req_path = ROOT_DIR / "requirements.txt"
        self.assertTrue(req_path.exists(), "Root requirements.txt should exist.")
        
        content = req_path.read_text(encoding="utf-8")
        lines = [line.strip().lower() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        
        expected_tools = ["requests", "bs4", "pandas", "numpy", "jupyter", "nbconvert"]
        for tool in expected_tools:
            self.assertTrue(
                any(tool in line for line in lines),
                f"Expected tooling dependency '{tool}' in root requirements.txt"
            )

    def test_monolithic_subproject_packages_excluded(self):
        req_path = ROOT_DIR / "requirements.txt"
        content = req_path.read_text(encoding="utf-8")
        lines = [line.strip().lower() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        
        forbidden_packages = ["torch", "torchvision", "ultralytics", "streamlit", "opencv-python-headless"]
        for pkg in forbidden_packages:
            self.assertFalse(
                any(pkg in line for line in lines),
                f"Subproject heavy package '{pkg}' should not be in root requirements.txt"
            )

    def test_update_requirements_script_removed(self):
        script_path = ROOT_DIR / ".github" / "scripts" / "update_requirements.py"
        self.assertFalse(
            script_path.exists(),
            ".github/scripts/update_requirements.py should be removed to prevent monolithic aggregation."
        )

if __name__ == "__main__":
    unittest.main()
