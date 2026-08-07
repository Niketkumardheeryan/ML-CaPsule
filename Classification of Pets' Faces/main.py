"""
Project Entry Point
"""

import os
import subprocess


def run_dashboard():

    os.system(
        "streamlit run app.py"
    )

    subprocess.run(
        [
            "streamlit",
            "run",
            "app.py"
        ]
    )

if __name__ == "__main__":
    run_dashboard()