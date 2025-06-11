# Labra — Lightweight Automation & Baseline Reporting Architecture

Labra is a proof-of-concept framework that combines a simple Python test runner with optional reporting services. It is aimed at teams that want a lightweight starting point for automation while still being able to grow into a more complete continuous integration setup.

## Features

- **Plugin-style runner** – `src/labra/testengine.py` loads configuration from `config/config.yaml` and executes tests using `pytest`.
- **Multiple test scopes** – tests are organised under `test/unit`, `test/integration` and `test/e2e` and can be filtered with pytest markers.
- **Docker demo stack** – `demo_infra/docker-compose.yaml` provisions GitLab CE, Allure reporting, Prometheus and Grafana for local experimentation.
- **GitLab pipeline** – the example `.gitlab-ci.yml` installs dependencies, runs the tests and uploads the resulting Allure report.

## Repository layout

```
├── config/                 # YAML configuration used by the runner
├── demo_infra/             # docker‑compose stack for demo infrastructure
├── src/labra/              # test runner and reusable task helpers
├── test/                   # unit, integration and e2e tests
└── requirements.txt        # Python dependencies
```

`src/labra/tasks/` contains small helper classes for the Playwright API and browser tasks used in the integration tests. These are intentionally minimal but show how additional tasks could be added.

## Getting started

1. Install Python 3.11 and pip.
2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   playwright install  # installs browser binaries for Playwright
   ```

3. Optionally start the demo services (Allure, GitLab, Prometheus and Grafana):

   ```bash
   docker compose -f demo_infra/docker-compose.yaml up -d
   ```

4. Run the tests using the provided configuration:

   ```bash
   python src/labra/testengine.py --config config/config.yaml
   ```

Test results will be written to the directory defined in the configuration file (by default `output/`). When the Allure service is running the runner will automatically post the results and trigger report generation.

## Configuration

`config/config.yaml` controls which test scopes are executed and how results are reported. The key options are:

- `enabled_scope` – list of pytest markers to include.
- `engine.test_root` – directory that pytest should start in.
- `reporting.allure_enabled` – whether to upload results to Allure.
- `reporting.allure_service` – URL of the Allure Docker Service.

Feel free to adjust these values to match your environment.

## Status

The project is intentionally small and many of the tests are placeholders. It acts as a template showing how a minimal automation framework can be assembled with Python, Playwright and standard DevOps tooling.

