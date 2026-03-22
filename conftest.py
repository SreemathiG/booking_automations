"""
conftest.py
===========
Pytest configuration file.
- Loads environment variables from .env
- Provides session-scoped config and test_data fixtures
- Provides function-scoped driver fixture (one fresh browser per test)
- Implements screenshot-on-failure hook
"""

import pytest
import yaml
import json
import os

from dotenv import load_dotenv
from utils.driver_factory import get_driver
from utils.screenshot import take_screenshot
from utils.logger import get_logger

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

logger = get_logger("conftest")


# ─────────────────────────────────────────────────────────────────
# SESSION FIXTURE: config
# Loaded once for the entire test session.
# Merges config.yaml with environment variables from .env
# ─────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def config():
    config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")

    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Environment variables override yaml values
    cfg["base_url"] = os.getenv("BASE_URL", "https://www.booking.com/")
    cfg["browser"]  = os.getenv("BROWSER", "chrome")
    cfg["timeout"]  = int(os.getenv("TIMEOUT", 15))

    logger.info(
        f"Config loaded — browser: {cfg['browser']} | "
        f"base_url: {cfg['base_url']} | timeout: {cfg['timeout']}s"
    )
    return cfg


# ─────────────────────────────────────────────────────────────────
# SESSION FIXTURE: test_data
# Reads AI-generated JSON file once per session.
# Raises a clear error if file has not been generated yet.
# ─────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def test_data():
    data_path = os.path.join(os.path.dirname(__file__), "test_data", "search_data.json")

    if not os.path.exists(data_path):
        raise FileNotFoundError(
            "\n\n"
            "  test_data/search_data.json not found!\n"
            "  Generate it first by running:\n\n"
            "      python -m ai_generator.generate_test_data\n"
        )

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    logger.info(f"Test data loaded — {len(data)} cases from search_data.json")
    return data


# ─────────────────────────────────────────────────────────────────
# FUNCTION FIXTURE: driver
# Creates a fresh browser instance for every test.
# This is required for parallel execution with pytest-xdist.
# Each worker gets its own isolated browser.
# ─────────────────────────────────────────────────────────────────
@pytest.fixture
def driver(config):
    d = get_driver(config["browser"])
    d.set_page_load_timeout(int(config["timeout"]) + 15)
    d.implicitly_wait(0)  # We rely on explicit waits only
    d.get(config["base_url"])
    logger.info(f"Browser opened: {config['base_url']}")

    yield d

    logger.info("Closing browser")
    d.quit()


# ─────────────────────────────────────────────────────────────────
# HOOK: Screenshot on failure
# Automatically captures a screenshot whenever a test fails.
# Saved to reports/screenshots/<test_name>_<timestamp>.png
# ─────────────────────────────────────────────────────────────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            take_screenshot(driver, item.name)
            logger.error(f"FAILED: {item.name} — screenshot captured")