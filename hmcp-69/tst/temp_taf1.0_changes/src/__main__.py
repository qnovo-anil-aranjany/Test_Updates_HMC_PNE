"""Main module for executing Test Automated Framework.

This is the main module/script that serves as the entry point for running various test
automation scripts, including making builds, static analysis, test cases, and coverage.
"""
from common import run_venv
from common.paths import (
    SCRIPT_COVERAGE,
    SCRIPT_MAKE,
    SCRIPT_PREPROCESS,
    SCRIPT_STATIC_ANALYSIS,
    SCRIPT_TEST_CASES,
)


def main() -> None:
    """
    Main function to run various test automation scripts.

    Executes scripts for pre-processing source, build, static analysis,
    test execution, and coverage analysis.
    """

    #run_venv(f"python {SCRIPT_PREPROCESS}")
    run_venv(f"python {SCRIPT_MAKE}")
    #run_venv(f"python {SCRIPT_STATIC_ANALYSIS}")
    #run_venv(f"python {SCRIPT_TEST_CASES}")
    #run_venv(f"python {SCRIPT_COVERAGE}")


if __name__ == "__main__":
    main()
