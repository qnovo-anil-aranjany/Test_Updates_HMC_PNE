"""Test Utility Functions and Virtual Environment Management.

This module provides utility functions for test automation, result comparison, and report generation,
and other functionalities. It includes helper functions to run pytest on specified test paths, compare test results
with expected values, and activate virtual environments for executing Python scripts. Additionally, it handles the
generation of HTML reports for test outcomes.
"""

import json
import logging
import os
import types
from glob import glob
from itertools import product
from os import listdir, makedirs, remove, walk
from os.path import basename, dirname, exists, isfile, join, splitext
from pathlib import Path
from re import compile, search
from shutil import copy
from subprocess import run
from sys import exit
from types import ModuleType
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pytest
from cffi import FFI
from varname import argname

from .paths import (
    BUILDOUTPUTS_REPORTS_PATH,
    BUILDOUTPUTS_SWC_PATH,
    BUILDOUTPUTS_TST_PATH,
    CMAKE_PATH,
    PROJECT_PATH,
    VENV_ACTIVATE_PATH,
)
from .platform import GH_ACTIONS, LINUX, WINDOWS


def clean_dat_files(path):
    """Deletes all .dat files within a specified directory.

    Args:
        path: A string specifying the path to the directory from which
                        .dat files will be deleted.
    """

    # Create a pattern to match all .dat files
    pattern = join(path, "*.dat")

    # Find all .dat files in the specified directory
    dat_files = glob(pattern)

    # Delete each .dat file
    for file_path in dat_files:
        remove(file_path)


def clean_gcda_files() -> None:
    """Cleans up .gcda files from the build directory.

    Searches for .gcda files recursively in the build directory and deletes them.
    """

    gcda_files = glob(join(CMAKE_PATH, "**", "*.gcda"), recursive=True)

    for gcda_file in gcda_files:
        try:
            remove(gcda_file)
            logging.info(f"Deleted: {gcda_file}")
        except OSError as e:
            logging.error(f"Error deleting {gcda_file}: {e}")


def compare_result(
    expected: Any,
    actual: Any,
    var_name: str = None,
    rtol: float = 1e-3,
    atol: float = 1e-6,
) -> None:
    """Checks the result of a test against an expected value.

    Raises an AssertionError if the result indicates a runtime error or if
    the result does not match the expected value within the specified tolerance.

    Args:
        expected: The expected result to compare against.
        actual: The result obtained from the test.
        var_name: Name of the variable.
        rtol: The relative tolerance value for comparing floating-point values (default: 1e-3).
        atol: The absolute tolerance value for comparing floating-point values (default: 1e-6).

    Returns:
        None: This function returns None if the result matches the expected value within the tolerance.

    Raises:
        AssertionError: If a runtime error is detected or the result does not match the expected value within the
                        tolerance.
        AssertionError: If expected and actual values are not the same data type.
    """

    if var_name is None:
        var_name = argname("actual")

    err_msg = "<_FuncPtr object at 0x"

    if err_msg in str(actual):
        raise AssertionError("Segmentation fault or other runtime error occurred.")

    if type(expected) != type(actual):
        raise AssertionError(
            f"{var_name} | Expected and actual values must be of the same data type. Expected type: {type(expected)}, Actual type: {type(actual)}."
        )

    if (isinstance(expected, float) or isinstance(actual, float)) or (
        (isinstance(expected, list) or isinstance(actual, list))
        and (
            all(isinstance(x, float) for x in expected)
            or all(isinstance(x, float) for x in actual)
        )
    ):
        if isinstance(expected, list) or isinstance(actual, list):
            assert np.allclose(
                actual[: len(expected)], expected, rtol=rtol, atol=atol
            ), f"{var_name} | Expected Result is {expected}, but Actual Result was {actual[:len(expected)]}."
        else:
            assert np.allclose(
                actual, expected, rtol=rtol, atol=atol
            ), f"{var_name} | Expected Result is {expected}, but Actual Result was {actual}."
    else:
        if isinstance(expected, list) or isinstance(actual, list):
            assert (
                actual[: len(expected)] == expected
            ), f"{var_name} | Expected Result is {expected}, but Actual Result was {actual[:len(expected)]}."
        else:
            assert (
                actual == expected
            ), f"{var_name} | Expected Result is {expected}, but Actual Result was {actual}."

    logging.info(f"TEST RESULT: {var_name} | Expected = {expected}, Actual = {actual}.")


def copy_with_ext(source_dir, target_dir, extension):
    """Copy files with the given extension from source_dir to target_dir.

    Args:
        source_dir : Path to the source directory.
        target_dir: Path to the target directory.
        extension: File extension to filter by (including the dot, e.g., '.so').
    """
    # Ensure the target directory exists
    makedirs(target_dir, exist_ok=True)

    # List all files and directories in the source directory
    for item in listdir(source_dir):
        # Construct full path to item
        item_path = join(source_dir, item)
        # Check if it's a file
        if isfile(item_path):
            # Check if the file has the desired extension
            if splitext(item)[1] == extension:
                # Construct target path and copy file
                copy(item_path, join(target_dir, item))


def get_key_in_nested_attr(
    lib: object, attr_path: str
) -> Tuple[Optional[object], Optional[str]]:
    """Retrieves the parent object and the last key name in a nested attribute path.

    Args:
        lib: The object to navigate through.
        attr_path: The complete dot-separated string representing the attribute path.

    Returns:
        Tuple: A tuple containing the parent object and the last attribute's name if the path is valid, otherwise (
               None, None).
    """

    keys = attr_path.split(".")
    current_attr = lib

    for key in keys[:-1]:
        if not hasattr(current_attr, key):
            return None, None
        current_attr = getattr(current_attr, key)

    return (current_attr, keys[-1]) if hasattr(current_attr, keys[-1]) else (None, None)


def get_lib_callables(lib: ModuleType) -> Dict[str, List[str]]:
    """Retrieve callables and non-callables from a cffi loaded dynamic link library (.dll/.so) object.

    This function analyzes the attributes of a shared library loaded via the cffi library and categorizes them into
    callable functions, callable variables, non-callable functions, and non-callable variables based on their
    characteristics and accessibility.

    Args:
        lib (FFIType): The shared library object loaded through cffi's FFI interface.

    Returns:
        dict_attr: A dictionary containing categorized attributes.
                   The keys are 'Callable Functions', 'Callable Variables',
                   'Non-Callable Functions', and 'Non-Callable Variables'.
                   Each key maps to a list of attribute names that fall
                   into that category.

    Raises:
        AttributeError: If an attribute is a non-callable function.
        KeyError: If an attribute is a non-callable variable.
    """

    ffi = FFI()

    callable_functions = "Callable Functions"
    callable_variables = "Callable Variables"
    non_callable_functions = "Non-Callable Functions"
    non_callable_variables = "Non-Callable Variables"

    dict_attr = {
        callable_functions: [],
        callable_variables: [],
        non_callable_functions: [],
        non_callable_variables: [],
    }

    attributes = dir(lib)

    for attr in attributes:
        try:
            attribute = getattr(lib, attr)

            if callable(attribute):
                type_str = str(ffi.typeof(attribute))
                if "(" in type_str and ")" in type_str:
                    dict_attr[callable_functions].append(attr)
                else:
                    dict_attr[callable_variables].append(attr)

                if isinstance(attribute, dict):
                    for key in attribute:
                        print(f"    Key in '{attr}': {key}")

        except AttributeError as ae:
            if "function" in str(ae).lower():
                dict_attr[non_callable_functions].append(attr)

        except KeyError as ke:
            if "variable" in str(ke).lower():
                dict_attr[non_callable_variables].append(attr)

    return dict_attr


def invoke_pytest(tst_path: Path, html: bool = False) -> None:
    """Invoke pytest for a given test path and generate an HTML report.

    The function runs pytest on the specified test path. It generates an HTML report
    named after the component being tested, which is inferred from the test path.

    Args:
        tst_path: The path to the test file or directory.
        html: If true, allow html report generation.

    Returns:
        None: The function will exit the process with the pytest exit code if it is non-zero.
    """

    # Infer the component name from the test path and set the report file name
    component = basename(dirname(tst_path))
    report_filename = f"Qnovo_Test_Summary_{component}.html"

    args = [
        "-vv",
        "-rs",
        "--tb=line",
        "--capture=no",
        "--self-contained-html",
        tst_path,
    ]

    if html:
        args.append(f"--html={join(BUILDOUTPUTS_REPORTS_PATH, report_filename)}")

    # Run pytest and generate an HTML report
    result = pytest.main(args)

    # If pytest results in an error, exit with the same exit code
    if result:
        exit(result)


def lib_array_to_list(attr):
    """Converts a CFFI array to a Python list if possible, otherwise returns the attribute unchanged.

    Args:
        attr: The attribute to convert, potentially a CFFI array.

    Returns:
        The converted Python list if `attr` was a CFFI array, otherwise `attr` itself.
    """

    try:
        return list(attr)
    except TypeError:
        return attr


def load_param_results_data(module_path: str) -> list:
    """Loads test data from a JSON file located in the "json" directory, named with a suffix based on the module's
    relationship to a specific parent directory.

    Args:
        module_path: The file path of the test module.

    Returns:
        list: A list of dictionaries, each representing a logged test case.
    """

    dir_name = "json"
    param_file_prefix = "param_results"
    test_file_prefix = "test_"

    module_name = basename(module_path)
    module_base, module_ext = splitext(module_name)

    parts = module_base.split(test_file_prefix, 1)

    if len(parts) > 1:
        json_suffix = parts[1]
    else:
        raise ValueError(f"Parameter results for {module_base} does not exist.")

    json_file_name = f"{param_file_prefix}_{json_suffix}.json"

    expected_results_dir = join(dirname(module_path), dir_name)
    file_path = join(expected_results_dir, json_file_name)

    makedirs(expected_results_dir, exist_ok=True)

    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def log_stack_parametrized_inputs(test_cases: Dict[str, str]) -> None:
    """Logs the description of a stack-parametrized test case.

    This function logs the description of the test case, which is specified under the 'Descriptions' key within the
    'test_cases' dictionary. It formats the output to clearly indicate the start of a new parametrized test case input.

    Args:
        test_cases: A dictionary containing the test case data, including a
                    'Descriptions' key with the description of the test case.
    """
    logging.info(f"\n\nParametrized Inputs:\n{test_cases['Descriptions']}\n")


def record_test_data(
    lib: Any,
    test_cases: Dict[str, Any],
    data_collector,
    var_to_record: List[str] = None,
    dict_to_record: Dict[str, Any] = None,
) -> None:
    """Constructs test data dictionary dynamically from specified variables and accumulates it for later logging.

    Args:
        lib: The library/module with attributes to be tested.
        test_cases: Test case data, including 'Descriptions' for test_id.
        var_to_record: List of variable to record from 'lib'.
        dict_to_record: Dictionary of variable and values to record that are not from 'lib'.
        data_collector: Function to accumulate test data for later logging.
    """

    test_data = {"test_id": test_cases["Descriptions"]}

    if var_to_record:
        for var in var_to_record:
            target_attr, target_key = get_key_in_nested_attr(lib, var)

            if target_attr and target_key:
                test_data[var] = lib_array_to_list(getattr(target_attr, target_key))
            else:
                pytest.fail(f"lib does not have attribute '{var}'")

    if dict_to_record:
        for key, value in dict_to_record.items():
            test_data[key] = value

    data_collector(test_data)


def parametrize_args(
    params: Dict[str, List[Any]]
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Prepares arguments for pytest.mark.parametrize by generating all combinations of named parameters
    encapsulated in dictionaries with corresponding IDs. Each test case dictionary includes the parameters
    under 'Inputs' and a descriptive string under 'Descriptions'.

    Args:
        params: A dictionary where each key is a parameter name and each value is a list of parameter values.

    Returns:
        output: A list of dictionaries, each dictionary represents a test case with 'Inputs' and 'Descriptions'.
        ids: A list of strings, each representing an ID for the corresponding test case.
    """

    inputs_name = "Inputs"
    description_name = "Descriptions"
    id_name = "id"
    id_prefix = "Param_Case"

    all_combinations = list(product(*params.values()))

    output = []
    ids = []

    for i, combo in enumerate(all_combinations, start=1):
        id_value = f"{id_prefix}_{i}"
        ids.append(id_value)

        combo_dict = {name: value for name, value in zip(params.keys(), combo)}
        description_parts = [f"\t{id_name}_{i}"] + [
            f"\t{name} = {value}" for name, value in combo_dict.items()
        ]
        #description = "\n".join(description_parts)
        description = f"{id_name}_{i}"

        output.append({inputs_name: combo_dict, description_name: description})

    return output, ids


def print_lib_callables(lib: types.ModuleType) -> None:
    """Prints the callable and non-callable attributes of a given library.

    Utilizes the 'get_lib_callables' function to categorize and then print the
    attributes of the provided shared library.

    Args:
        lib: The shared library whose attributes are to be printed.
    """

    attribute_categories = get_lib_callables(lib)
    print("\n")
    for category, items in attribute_categories.items():
        print(f"{category}: {items}")


def run_venv(command: str) -> int:
    """This function activates a specified virtual environment and runs given Python scripts.

    Checks the running environment and executes the command either locally on Windows/Linux or
    within GitHub Actions running on Windows. In other environments, it raises an error.

    Args:
        command: A string specifying the command to be executed in the virtual environment.

    Returns:
        int: The exit code returned by the executed command.

    Raises:
        EnvironmentError: If the script is not running in a Windows or Linux environment locally or in GitHub
        Actions.
    """

    if WINDOWS:
        if GH_ACTIONS:
            result = run(command)  # GitHub Actions running on Windows
        else:
            result = run(f"{VENV_ACTIVATE_PATH}.bat && {command}")  # local Windows env
    elif LINUX:
        result = run(f"{command}", shell=True)  # local Linux env
    else:
        raise EnvironmentError(
            "Unsupported environment: This script can only be run on Windows or Linux."
        )

    return result.returncode


def set_lib_inputs(lib: ModuleType, test_cases: Any) -> None:
    """Sets values to the variables in the shared library based on the provided test cases,
    including nested attributes.

    This function iterates over the "Inputs" dictionary within the test_cases argument.
    For each key-value pair in "Inputs", it navigates through the lib module's attributes,
    handling both top-level and nested attributes, to set the corresponding value.

    Args:
        lib: The shared library on which to set attributes values (i.e. the variables in the C code).
        test_cases: A dictionary containing test case data, including an "Inputs" dictionary.
    """
    for input_key, input_value in test_cases["Inputs"].items():
        target_attr, target_key = get_key_in_nested_attr(lib, input_key)

        if target_attr and target_key:
            setattr(target_attr, target_key, input_value)


def size(lib: list[int]) -> int:
    """Calculates and returns the size of a statically allocated array defined in the shared library 'lib'.

    This function extracts the size (number of elements) of an array from its ctype type string representation.
    It assumes the array is statically allocated with a fixed size, as indicated by its type definition.

    Args:
        lib: A CFFI loaded shared library object representing an array, where `FFIType` is a placeholder
             for the actual CFFI type.

    Returns:
        int: The number of elements in the array as defined by its type.

    Raises:
        ValueError: If the type string does not contain size information in the expected format.
    """

    ffi = FFI()
    type_str = ffi.getctype(ffi.typeof(lib))

    try:
        # Initialize an empty list to hold sizes
        sizes = []
        # Split the string on '[' and iterate over the results, ignoring the first split (base type)
        for part in type_str.split("[")[1:]:
            # Each part now looks like "10]" or "20]", strip the "]" and convert to int
            size = int(part.rstrip("]"))
            sizes.append(size)

        # Return the appropriate size format based on the number of dimensions
        return sizes[0] if len(sizes) == 1 else sizes
    except ValueError as e:
        raise ValueError(
            "The provided CFFI object does not have a statically defined size."
        ) from e


def validate_test_cases(
    lib: Any,
    test_cases: Any,
    expected_param_results: Any = None,
    dict_to_compare: Dict[Any, str] = None,
    rtol: float = 1e-3,
    atol: float = 1e-6,
) -> None:
    """Validates a test case expected results against actual results.

    Args:
        lib: The shared library with attributes to be tested.
        test_cases: Test case data with "Expected" values or a "Descriptions" key.
        expected_param_results: Expected results from json file.
        dict_to_compare: Dictionary of desired variables for comparison, that are not in 'lib'.
        rtol: The relative tolerance value for comparing floating-point values (default: 1e-3).
        atol: The absolute tolerance value for comparing floating-point values (default: 1e-6).
    """
    if "Expected" in test_cases:
        ref_data = test_cases["Expected"]
    else:
        test_id = "t"+test_cases["Descriptions"]
        print(f"\n Test ID: {test_id}")
        ref_data = expected_param_results.get(test_id)
        print(f"\n: Expected: {expected_param_results}")

        if not ref_data:
            pytest.fail(f"No test data found for test_id: {test_id}")

    for key, expected_value in ref_data.items():
        if key != "test_id":
            if dict_to_compare and key in dict_to_compare:
                compare_result(expected_value, dict_to_compare[key], key, rtol, atol)
            else:
                target_attr, target_key = get_key_in_nested_attr(lib, key)

                if target_attr and target_key:
                    actual_value = lib_array_to_list(getattr(target_attr, target_key))
                    compare_result(expected_value, actual_value, key, rtol, atol)
                elif target_key is None:
                    pytest.fail(f"No attribute '{key}' found.")


class FileProcessor:
    """This class provides methods to search for files within a specified directory structure
    based on given extensions and header files. It can also optionally copy the matched files
    to predefined directories based on their names.

    Attributes:
        test_config_name (str): The name of the test configuration directory.
        test_harness_name (str): The name of the test harness directory.
        products_api_repo_name (str): The name of the products API repository directory.
        dependencies_dir_name (str): The name of the repo dependencies directory.
        config_json_name (str): The name of the configuration JSON file.
        json_key_name (str): The name of the JSON key holding the target directories.
    """

    def __init__(self):
        self.buildoutputs_swc_path = BUILDOUTPUTS_SWC_PATH
        self.buildoutputs_tst_path = BUILDOUTPUTS_TST_PATH
        self.test_config_name = "test_config"
        self.test_harness_name = "test_harness"
        self.products_api_repo_name = "sp_products_api"
        self.dependencies_dir_name = "dependencies"
        self.config_json_name = "sp_products_api_target.json"
        self.json_key_name = "testing_config"

    def process_files(
        self,
        base_directory: str,
        extensions: Union[str, List[str]],
        header_list: List[str] = None,
        copy_files: bool = False,
    ) -> List[str]:
        """Process files in a given directory matching specified extensions.

        This method searches for files within the given base directory that match the specified
        extensions. If it encounters the "sp_products_api" directory, it reads the configuration
        from the "config.json" file to determine the subdirectory to focus on. It can optionally
        copy the matched files to predefined directories based on their names.

        Args:
            base_directory (str): The base directory to search for files.
            extensions (Union[str, List[str]]): A single extension or a list of extensions to match.
            header_list (List[str], optional): A list of header file names to match. Defaults to None.
            copy_files (bool, optional): A flag to determine whether to copy files. Defaults to False.

        Returns:
            List[str]: A list of file paths for files that match the given extensions.

        Raises:
            FileNotFoundError: If the "sp_products_api" directory exists but the "config.json" file is not found.
            KeyError: If the "target_dirs" key is not found in the "config.json" file.
            FileNotFoundError: If the specified "target_dirs" directory does not exist.
        """

        if isinstance(extensions, str):
            extensions = [extensions]

        file_paths = []
        config_found = False
        base_dir_depth = base_directory.count(os.sep)

        for root, dirs, _ in walk(base_directory, followlinks=True):
            dirs[:] = [d for d in dirs if d != ".git"]

            if self.products_api_repo_name not in root:
                file_paths.extend(
                    self._process_directory(root, extensions, header_list, copy_files)
                )
                continue

            dependencies_dir = dirname(root)
            dependencies_dir_depth = dependencies_dir.count(os.sep)

            if (
                dependencies_dir.count(self.dependencies_dir_name) != 1
                or dependencies_dir_depth - base_dir_depth != 1
            ):
                continue

            if not config_found:
                config_path = join(dependencies_dir, self.config_json_name)
                if not exists(config_path):
                    raise FileNotFoundError(
                        f"{self.products_api_repo_name} exists but {self.config_json_name} file not found at: {config_path}"
                    )

                with open(config_path) as f:
                    config = json.load(f)

                target_dirs = config.get(self.json_key_name)
                if target_dirs is None:
                    raise KeyError(
                        f"{self.json_key_name} key not found in {self.config_json_name}"
                    )

                target_dir = join(root, *target_dirs)
                if not exists(target_dir):
                    raise FileNotFoundError(
                        f"Specified {self.json_key_name} directory does not exist: {target_dir}"
                    )

                config_found = True

            file_paths.extend(
                self._process_directory(target_dir, extensions, header_list, copy_files)
            )

        return file_paths

    def _process_directory(self, directory, extensions, header_list, copy_files):
        """Intermediate step to process files in a specific directory.

        This method processes files in the given directory that match the specified extensions
        and header files. It can optionally copy the matched files to predefined directories
        based on their names.

        Args:
            directory (str): The directory to process files from.
            extensions (List[str]): A list of extensions to match.
            header_list (List[str]): A list of header file names to match.
            copy_files (bool): A flag to determine whether to copy files.

        Returns:
            List[str]: A list of file paths for files that match the given extensions and header files.
        """

        file_paths = []
        project_path = str(PROJECT_PATH)

        if (
            directory.count(os.sep) <= project_path.count(os.sep) + 2
            or basename(directory) == "dependencies"
        ):
            return file_paths

        for root, _, files in walk(directory, followlinks=True):
            for file in files:
                if not any(file.endswith(ext) for ext in extensions):
                    continue

                file_path = join(root, file)

                if header_list is not None:
                    if file.endswith(".h"):
                        if file not in header_list:
                            continue
                    elif self.dependencies_dir_name in file_path:
                        continue

                file_paths.append(file_path)

                if copy_files:
                    self._copy_file(file_path)

        return file_paths

    def _copy_file(self, file_path):
        """Copy a file to a predefined directory based on its name.

        This method copies the given file to a predefined directory based on its name.
        If the file name contains 'test_config' or 'test_harness', it is copied to the
        BUILDOUTPUTS_TST_PATH directory. Otherwise, it is copied to the BUILDOUTPUTS_SWC_PATH
        directory.

        Args:
            file_path (str): The path of the file to copy.
        """
        if any(
            test_string in file_path
            for test_string in [self.test_config_name, self.test_harness_name]
        ):
            makedirs(self.buildoutputs_tst_path, exist_ok=True)
            copy(file_path, self.buildoutputs_tst_path)
        else:
            makedirs(self.buildoutputs_swc_path, exist_ok=True)
            copy(file_path, self.buildoutputs_swc_path)


class HeaderExtractDeclarations:
    """Processes header files to extract declarations for cffi.

    Attributes:
        extern_flag: A string flag used to identify extern declarations.
        define_pattern: A compiled regular expression to identify macro definitions.
    """

    def __init__(self):
        self.extern_flag = "/* _extern_ */"
        self.define_pattern = compile(r"#define\s+(\w+)\s+([^/]+)")

    def read_from_file(self, file_path: str) -> List[str]:
        """Reads lines from a file.
        Args:
            file_path: The path to the file to be read.
        Returns:
            A list of lines from the file.
        """
        with open(file_path, "r") as file:
            return file.readlines()

    def add_externs(self, lines: List[str]) -> List[str]:
        """
        Args:
            lines: A list of lines in which to add 'extern'.
        Returns:
            A list of updated lines with 'extern' added where applicable.
        """
        updated_lines = []
        for line in lines:
            if self.extern_flag in line:
                updated_line = "extern " + line.replace(self.extern_flag, "")
            else:
                updated_line = line
            updated_lines.append(updated_line)
        return updated_lines

    def process_multiline_macro(self, lines: List[str]) -> List[str]:
        """Join multiline macros into single lines.
        Args:
            lines: A list of lines to preprocess.
        Returns:
            preprocessed_lines: A list of preprocessed lines with multiline macros joined into single lines.
        """
        preprocessed_lines = []
        current_line = ""
        for line in lines:
            if line.strip().endswith("\\"):
                current_line += line.strip()[:-1]
            else:
                current_line += line.strip()
                preprocessed_lines.append(current_line)
                current_line = ""
        return preprocessed_lines

    def extract_macros(self, lines: List[str]) -> Dict[str, str]:
        """Collect a dictionary of macros from the header files.
        Args:
            lines: A list of lines potentially containing macro definitions.
        Returns:
            A dictionary of macro names and their corresponding values.
        """
        preprocessed_lines = self.process_multiline_macro(lines)
        macros = {}
        for line in preprocessed_lines:
            match = self.define_pattern.match(line)
            if match:
                macros[match.group(1)] = match.group(2).strip()
        return macros

    def extract_declarations(self, lines: List[str], macros: Dict[str, str]) -> str:
        """
        Args:
            lines: A list of lines from which to extract declarations.
            macros: A dictionary of macro definitions to replace in lines.
        Returns:
            A string containing the processed declarations.
        """
        processed_lines = []
        for line in lines:
            if not line.strip().startswith(("#", "//")):
                for old, new in macros.items():
                    line = line.replace(old, new)
                line = line.replace("const ", "")
                processed_lines.append(line)

        filtered_lines = [
            line
            for line in processed_lines
            if not line.startswith("//")
            and not line.strip() == ""
            and not line.strip().startswith("(")
            and not line.strip().startswith(")")
            and not line.strip().startswith("{")
            and not line.strip().startswith("_")
            and not (
                line.strip() == "}"
                or line.strip().startswith("}")
                and not line.strip().endswith(";")
            )
            and not line.strip().startswith("_Pragma")
        ]

        output = "".join(filtered_lines).strip()
        return output

    def get_declarations(self, header_files: List[str]) -> str:
        """
        Args:
            header_files: A list of paths to the header files.
        Returns:
            A string containing all processed declarations from the header files.
        """

        # Extract header file contents
        header_files_content = [
            line
            for file_path in header_files
            for line in self.read_from_file(file_path)
        ]

        # Extract declaration for cdef
        externs = self.add_externs(header_files_content)
        macros = self.extract_macros(externs)
        declarations = self.extract_declarations(externs, macros)

        return declarations


class HeaderDependencyOrder:
    """
    Analyze the dependencies between header files and provide the dependency order.

    Args:
       directory (str): The directory path containing the header files.

    Attributes:
       directory (str): The directory path containing the header files.
       header_files (list): A list of header file paths.
       dependency_graph (dict): A dictionary representing the dependency graph of header files.
       ordered_headers (list): A list of header files in the dependency order.

    Methods:
       get_header_files(): Retrieves all header files in the specified directory and its subdirectories.
       extract_includes(file_path): Extracts the #include directives that include other header files from a given header file.
       build_dependency_graph(): Constructs the dependency graph of header files.
       get_dependency_order(): Determines the dependency order of header files using depth-first search (DFS).
       get_ordered_headers(): Returns the list of header files in the dependency order.
    """

    def __init__(self, directory):
        self.directory = directory
        self.header_files = self.get_header_files()
        self.dependency_graph = self.build_dependency_graph()
        self.ordered_headers = self.get_dependency_order()

    def get_header_files(self):
        header_files = []
        for root, dirs, files in walk(self.directory, followlinks=True):
            for file in files:
                if file.endswith(".h"):
                    header_files.append(join(root, file))
        return header_files

    def extract_includes(self, file_path):
        includes = []
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("#include"):
                    match = search(r'"(.*?)"', line)
                    if match:
                        included_file = match.group(1)
                        if included_file.endswith(".h"):
                            includes.append(included_file)
        return includes

    def build_dependency_graph(self):
        header_dict = {}
        for header_file in self.header_files:
            header_dict[basename(header_file)] = header_file

        dependency_graph = {}
        for header_file in self.header_files:
            includes = self.extract_includes(header_file)
            dependency_graph[header_file] = [
                header_dict[include] for include in includes if include in header_dict
            ]

        return dependency_graph

    def get_dependency_order(self):
        visited = set()
        ordered_headers = []

        def dfs(header_file):
            visited.add(header_file)
            for dependency in self.dependency_graph[header_file]:
                if dependency not in visited:
                    dfs(dependency)
            ordered_headers.append(header_file)

        for header_file in self.header_files:
            if header_file not in visited:
                dfs(header_file)

        return ordered_headers

    def get_ordered_headers(self):
        return self.ordered_headers

def iter_file(file_path):
    """Works for .csv and Excel files (.xlsx, .xls, .xlsb, .ods)"""
    print(f"\niter_file {file_path}")
    import csv
    from python_calamine import CalamineWorkbook

    if file_path.endswith(".csv"):
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield row
    elif file_path.endswith((".xlsx", ".xls", ".xlsb", ".ods")):
        workbook = CalamineWorkbook.from_path(file_path)
        rows = iter(workbook.get_sheet_by_index(0).to_python())
        headers = list(map(str, next(rows)))
        for row in rows:
            yield dict(zip(headers, row))
        workbook.close()
    else:
        raise ValueError(
            f"Unsupported file format: {file_path}. Supported formats: .csv, .xlsx, .xls, .xlsb, .ods"
        )

def validate_with_reference_data(output_file_path, reference_file_path):
    """
    Compare two Excel files for validation.

    Args:
        output_file_path: Path to the output Excel file
        reference_file_path: Path to the reference Excel file

    Returns:
        bool: True if files match, False otherwise
    """
    import pandas as pd
    try:
        output_df = pd.read_excel(output_file_path)
        ref_df = pd.read_excel(reference_file_path)

    except Exception as e:
        print(f"Error reading Excel files: {e}")
        return False

    # Check if DataFrames are equal using pandas built-in comparison
    try:
        # This handles NaN properly and gives detailed comparison
        pd.testing.assert_frame_equal(
            output_df,
            ref_df,
            check_dtype=True,  # Set False if you don't care about int vs float
            check_exact=False,  # Allow small floating point differences
            rtol=1e-6,  # Relative tolerance for floats
            atol=1e-6,  # Absolute tolerance for floats
        )
        return True

    except AssertionError as e:
        # Files don't match - log the differences
        print(f"Excel files do not generally match: {str(e)}")

        # Additional detailed comparison for debugging
        if output_df.shape != ref_df.shape:
            print(
                f"Column and row dimensions mismatch: Output {output_df.shape} vs Reference {ref_df.shape}"
            )

        if not output_df.columns.equals(ref_df.columns):
            print(
                f"Column headers mismatch: {list(output_df.columns)} vs {list(ref_df.columns)}"
            )

        # Show actual differences if shapes match
        if output_df.shape == ref_df.shape:
            comparison = output_df.compare(ref_df)
            if len(comparison) < 50:
                print(f"Differences:\n{comparison}")
            else:
                print(
                    f"Too many differences ({len(comparison)} rows): Manual comparison required"
                )

        return False

def write_output_to_csv(results, file_path, ap=False):
    import csv
    mode = "w"
    if ap == True:
        mode = "a"
    with open(file_path, mode, newline="") as csvfile:
        writer = csv.writer(csvfile)
        row = 0
        first = True
        for each_item in results:
            data_row = list(each_item.values())
            if first:
                row_data = list(each_item.keys())
                writer.writerow(row_data)
                first = False
            row += 1

            index = 0
            for item in data_row:
                if isinstance(item, list):
                    r = ""
                    for i in item:
                        r += str(i)
                        r += " "
                    r.strip("")
                    data_row[index] = r.strip(" ")
                else:
                    data_row[index] = item
                index += 1
            writer.writerow(data_row)