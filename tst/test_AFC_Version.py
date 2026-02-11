"""Test Module Description:
    Test module AFC versioning.

Requirements:
    - [JIRA ticket or requirement reference]
    - Python version >= 3.10.4
    - Pytest version >= 7.4.3
"""

from .main import *

# Optional Flags:
# ------------------------------------------------
SKIP_MODULE = False  # Set to True to skip all test cases in this module.

if SKIP_MODULE:
    pytestmark = pytest.mark.skip(reason="All test cases in this module are skipped.")


@pytest.mark.parametrize(
    "test_cases",
    [
        param(
            {
                "Inputs": {
                    "Major": 5,
                    "Minor": 8,
                    "Patch": 0,
                },
                "Expected": {
                    "version": 50600,
                },
            },
            id="TestQnovoVersion",
            marks=[
                mark.description("This test checks version of AFC software."),
            ],
        ),
    ],
)
@allure.feature(
    """
        Steps:\
        Step1: Have the source files ready for generating binary for swc_fast_charge.,\
        Step2: Generate binary (shared dll using cmake) using cmake,\
        Step3: Invoke method get_afc_sw_ver from afc binary via cffi using input param Le_T_CellTemp,\
        Step4: compare output with expected value from input param - NA,\
        Step5: Test result should match with expected value: 50600 (or check against current version),\

        Source_File_In_Test: swc_afc_algo.c
        Method_In_Test: QnovoAFC_SW_Version

        parent_suite: swc_fast_charge
        suite: afc_qnovo_afc_version
        sub_suite: qnovo_afc_version
    """
)
class TestQnovoVersion:
    def test_qnovo_afc_version(self, setup_parameters, test_cases) -> None:
        """
        This test function performs verification of the AFC version.
        """
