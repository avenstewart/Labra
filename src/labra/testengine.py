import argparse
import yaml
import pytest
from datetime import datetime
import requests
import base64
import json
from pathlib import Path


CONFIG_PATH_DEFAULT = "config/config.yaml"


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

def run_tests(test_root, scope, reports_dir, allure_enabled):

    args = [
        test_root,
        "-m", " and ".join(scope),
        "-v"
    ]
    if allure_enabled:
        args.append("--alluredir=" + reports_dir)

    print(args)
    return pytest.main(args)

def post_results_to_allure(allure_results_dir, project_id="default", service_url="http://localhost:5050"):
    allure_results_dir = Path(allure_results_dir).resolve()
    print("Preparing Allure results from:", allure_results_dir)

    # Check if project exists
    check_resp = requests.get(f"{service_url}/allure-docker-service/projects")
    try:
        projects_data = check_resp.json()
    except json.JSONDecodeError:
        raise RuntimeError(f"Failed to decode JSON from project list: {check_resp.text}")

    print("Project list response:", projects_data)  # Optional debug

    try:
        existing_projects = list(projects_data["data"]["projects"].keys())
    except (KeyError, TypeError):
        raise RuntimeError(f"Unexpected project list structure: {projects_data}")

    if project_id not in existing_projects:
        print(f"Creating project '{project_id}'...")
        create_resp = requests.post(
            f"{service_url}/allure-docker-service/projects",
            headers={'Content-Type': 'application/json'},
            json={"id": project_id},
            verify=True
        )
        if create_resp.status_code not in (200, 201):
            raise RuntimeError(f"Project creation failed: {create_resp.status_code} {create_resp.text}")

    # Prepare result files
    results = []
    for file_path in allure_results_dir.iterdir():
        if file_path.is_file():
            with open(file_path, "rb") as f:
                content = f.read()
                if content.strip():
                    encoded = base64.b64encode(content).decode("utf-8")
                    results.append({
                        "file_name": file_path.name,
                        "content_base64": encoded
                    })

    if not results:
        raise RuntimeError("No valid result files found to upload.")

    # Upload results
    headers = {'Content-Type': 'application/json'}
    request_body = {"results": results}
    response = requests.post(
        f"{service_url}/allure-docker-service/send-results?project_id={project_id}",
        headers=headers,
        data=json.dumps(request_body),
        verify=True
    )
    if response.status_code != 200:
        raise RuntimeError(f"Upload failed: {response.status_code} {response.text}")

    # Generate report
    response = requests.get(
        f"{service_url}/allure-docker-service/generate-report",
        params={
            "project_id": project_id,
            "execution_name": "LABRA test run",
            "execution_from": "http://localhost",
            "execution_type": "manual"
        },
        headers=headers,
        verify=True
    )
    if response.status_code != 200:
        raise RuntimeError(f"Report generation failed: {response.status_code} {response.text}")

    response_data = response.json()
    print("Allure report generated.")
    print("Report URL:", response_data["data"].get("report_url"))

def main():

    parser = argparse.ArgumentParser(description="Labra Test Runner")
    parser.add_argument("--config", default=CONFIG_PATH_DEFAULT, help="Path to YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report_path = f"output/report_{timestamp}.html"

    # Grab Config
    reporting_conf = config.get('reporting')
    engine_conf = config.get('engine')
    enabled_scope = config.get('enabled_scope')  # list
    environment_conf = config.get('environment')
    features_conf = config.get('features')

    output_folder = reporting_conf.get('output_dir')
    project_id = engine_conf.get('project_id')
    allure_service = reporting_conf.get('allure_service')
    allure_enabled = reporting_conf.get('allure_enabled', True),

    # Begin tests
    run_tests(
        test_root=config.get('engine').get('test_root'),
        scope=enabled_scope,
        reports_dir=output_folder,
        allure_enabled=allure_enabled,
    )

    print("Sending to:", f"{allure_service}/send-results")
    print("With project_id:", project_id)

    if allure_enabled:
        post_results_to_allure(output_folder, project_id, allure_service)


if __name__ == "__main__":
    main()
