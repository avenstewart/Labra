import pytest
import yaml
from src.labra.test_runner import load_config, discover_test_dirs, run_tests


@pytest.fixture
def sample_config():
    return {
        "enabled_tests": ["unit", "integration"]
    }

@pytest.fixture
def temp_config_file(tmp_path, sample_config):
    config_file = tmp_path / "config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(sample_config, f)
    return config_file


def test_load_config(temp_config_file, sample_config):
    config = load_config(temp_config_file)
    assert config == sample_config


def test_discover_test_dirs(sample_config, tmp_path):
    test_dirs = discover_test_dirs(sample_config)
    assert isinstance(test_dirs, list)
    assert all(isinstance(path, str) for path in test_dirs)


def test_run_tests(tmp_path):
    test_dirs = ["tests/unit"]
    html_report = str(tmp_path / "report.html")
    result = run_tests(test_dirs, html_report)
    assert isinstance(result, int)
    assert result in [0, 1]
