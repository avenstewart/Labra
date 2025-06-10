import argparse
import subprocess
import yaml
import os
import sys
from datetime import datetime

CONFIG_PATH_DEFAULT = "../../config/config.yaml"


def load_config(path):
    """
    Load YAML configuration from the specified path.

    Args:
        path (str): Path to the YAML config file.

    Returns:
        dict: Parsed configuration as a dictionary.
    """
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def discover_test_dirs(config):
    """
    Identify and return enabled test directories based on config.

    Args:
        config (dict): Loaded configuration specifying enabled tests.

    Returns:
        list[str]: List of valid test directory paths.
    """
    base_dir = "../../tests"
    enabled = config.get("enabled_tests", [])
    paths = [os.path.join(base_dir, d) for d in enabled if os.path.isdir(os.path.join(base_dir, d))]
    return paths


def run_tests(test_dirs, allure_enabled):

    """
    Execute pytest on the specified test directories and generate HTML report.

    Args:
        test_dirs (list[str]): Paths to test directories.
        use_allure (bool): Whether to generate Allure reports.

    Returns:
        int: Exit code returned by pytest process.
    """

    cmd = [
        sys.executable, "-m", "pytest",
        "--tb=short",
        "-v"
    ]

    if allure_enabled:
        cmd.append("--alluredir=output/allure-results")

    cmd.extend(test_dirs)
    return subprocess.call(cmd)


def main():
    """
    Main function to parse arguments, run test discovery and execution,
    and report results including HTML output location.
    """
    parser = argparse.ArgumentParser(description="Labra Test Runner")
    parser.add_argument("--config", default=CONFIG_PATH_DEFAULT, help="Path to YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    test_dirs = discover_test_dirs(config)
    if not test_dirs:
        print("No valid test directories found. Check your config.")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report_path = f"output/report_{timestamp}.html"

    print(f"Running tests in: {test_dirs}")
    use_allure = config.get('reporting', {}).get('use_allure', True)
    result = run_tests(test_dirs, html_report_path, use_allure)

    if result == 0:
        print("✅ All tests passed.")
    else:
        print("❌ Some tests failed.")

    print(f"Test report: {html_report_path} (saved to /output)")
    sys.exit(result)


if __name__ == "__main__":
    main()
