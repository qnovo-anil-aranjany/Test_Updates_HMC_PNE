"""Default module for pytest configurations and hooks.

This module customizes the pytest-html report by adding additional columns
for descriptions and JIRA links. It utilizes pytest hooks to modify the HTML
results table and to set report attributes based on custom markers.
"""
import os
from typing import List

import cffi
import pytest
from _pytest.config import Config
from _pytest.nodes import Item
from _pytest.reports import TestReport

from ..submodules.tool_test_automation.src.common.paths import (
    BUILDOUTPUTS_REPORTS_PATH,
    CMAKE_SCRIPT,
    PRE_PROCESS_SCRIPT,
    PROJECT_PATH,
)
from ..submodules.tool_test_automation.src.common.run_venv import (
    populate_envs,
    run_venv,
    update_envs,
)
from .main import ParamDict

JIRA_LINK = "https://qnovo.atlassian.net/browse/"
ffi = cffi.FFI()


def pytest_configure(config: Config) -> None:
    """Adjust the log level for console output to WARNING when running pytest.

    This function is a hook for pytest configuration that sets up the logging framework to capture INFO level messages
    across the application and ensures that only WARNING and above level messages are printed to the console. It
    replaces any existing logging handlers with a single console handler set for WARNING level, to reduce clutter in
    test output.

    Args:
        config (Config): The pytest configuration object, not directly used in this function but required by the hook
        signature.
    """
    print("CONFTEST")
    config.addinivalue_line("markers", "description: Description of a test case")
    config.addinivalue_line("markers", "jira_id: JIRA-ID of a test case")
    config.addinivalue_line(
        "markers", "run_exclusively: mark a test to run exclusively"
    )
    update_envs("BUILD_TYPE", "CUSTOMER_BUILD")
    update_envs("SW_COMPONENT", "")
    if populate_envs("SINGLE_RUN") is True:
        run_venv(f"python {PRE_PROCESS_SCRIPT}")
        run_venv(f"python {CMAKE_SCRIPT}")
    # initialize lib values once.
    pytest.paramdict = ParamDict().param_dict


def pytest_collection_modifyitems(config: Config, items: List[Item]) -> None:
    """Modifies the collection of items to run by simplifying test identifiers and optionally skipping tests.

    This hook is invoked after the collection phase to alter the list of collected test items. It performs two main
    functions:
    1. Simplifies test identifiers to only include the test function names, making the output more readable.
    2. Skips all tests not marked with @pytest.mark.run_exclusively if at least one test has that marker. This allows
       for selective test execution, focusing on tests deemed critical or under active development.

    Args:
        config (_pytest.config.Config): The pytest configuration object, providing access to command line options and
        other configuration.
        items (List[_pytest.nodes.Item]): A list of item objects representing the collected tests.
    """

    # Simplify the test name identifier to only include the test function name, remove the path names
    for item in items:
        simplified_id = item.nodeid.split("::")[-1]
        item._nodeid = simplified_id

    # Skips all tests not marked with @pytest.mark.run_exclusively
    run_exclusive_test = [
        item for item in items if item.get_closest_marker("run_exclusively")
    ]

    if run_exclusive_test:
        exclusive_test_ids = ", ".join(ex_item.nodeid for ex_item in run_exclusive_test)
        items_to_skip = [item for item in items if item not in run_exclusive_test]

        for item in items_to_skip:
            item.add_marker(
                pytest.mark.skip(
                    reason=f"@pytest.mark.run_exclusively on {exclusive_test_ids}"
                )
            )


def pytest_html_results_table_header(cells: List[str]) -> None:
    """Modify the HTML report table header to add custom columns.

    Args:
        cells (list): The list of HTML cells in the table header.
    """
    cells.insert(2, "<th>Description</th>")
    cells.insert(3, "<th>JIRA Link</th>")
    cells.pop()


def pytest_html_results_table_row(report: TestReport, cells: List[str]) -> None:
    """Modify the HTML report table rows to include custom data.

    Inserts custom data for the description and JIRA link into the report table based on the
    test report's attributes.

    Args:
        report (pytest.TestReport): The pytest report object.
        cells (list): The list of HTML cells in the table row.
    """
    cells.insert(2, f"<td>{report.description}</td>")
    cells.insert(
        3, f'<td><a href="{JIRA_LINK}{report.jira_id}">{report.jira_id}</a></td>'
    )
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Item, call: pytest.CallInfo) -> None:
    """Hook to process and augment the test report with custom attributes.

    Extracts information from custom markers and sets them as attributes on the test report.

    Args:
        item (pytest.Item): The test item.
        call (pytest.CallInfo): Call info for the test.
    """
    outcome = yield
    report = outcome.get_result()
    marker_names = ["description", "jira_id"]
    set_report_attributes_from_markers(item, report, marker_names)


def pytest_sessionstart(session):
    """Hook executed at the beginning of the pytest session.

    Deletes the test log JSON file to start fresh for the session.
    """
    file_name = "test_results.json"  # The name of your log file
    file_path = os.path.join(BUILDOUTPUTS_REPORTS_PATH, file_name)

    if os.path.exists(file_path):
        os.remove(file_path)


def pytest_sessionfinish(session, exitstatus):
    """
    Hook Executed to clean up actions after a pytest session.
    """
    # .coverage file is generated by pytest-cov, which we do not require.
    # python coverage data is written to buildoutputs/report
    cov_file = PROJECT_PATH / ".coverage"
    if os.path.exists(cov_file):
        os.remove(cov_file)


def set_report_attributes_from_markers(
    item: Item, report: TestReport, marker_names: List[str]
) -> None:
    """Sets attributes on the report object based on specified marker names.

    For each marker name in the list, attempts to find the marker on the test item and sets
    corresponding attributes on the report object.

    Args:
        item: The test item.
        report: The test report object.
        marker_names: A list of marker names to look for and set on the report.
    """
    for marker_name in marker_names:
        marker = item.get_closest_marker(marker_name)
        if marker:
            setattr(report, marker_name, marker.args[0])
        else:
            setattr(report, marker_name, "")
