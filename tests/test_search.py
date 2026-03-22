"""
test_search.py
==============
Main test file for the Booking.com automation framework.

Test flow:
  1. Search for a location (from AI-generated test data)
  2. Validate search results are returned
  3. Open the first hotel's detail page
  4. Click the Reserve button (equivalent to Add to Cart)

AI Data Architecture:
  - test_data/search_data.json is generated ONCE by running:
        python -m ai_generator.generate_test_data
  - Tests read from this file at module load time
  - Zero API calls happen during test execution (fast + stable)
  - Each parametrized test case = one AI-generated location

Parallel Execution:
  - Each test gets its own driver (function-scoped fixture)
  - Safe to run with: pytest -n auto
"""

import json
import os
import pytest

from pages.home_page import HomePage
from pages.results_page import ResultsPage
from pages.hotel_page import HotelPage
from utils.logger import get_logger

logger = get_logger("test_search")


# ─────────────────────────────────────────────────────────────────
# Load AI-generated test data at module level.
# This happens once when pytest collects tests — not during execution.
# No network call. Pure file read. Instantly fast.
# ─────────────────────────────────────────────────────────────────
def _load_cases():
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "test_data",
        "search_data.json"
    )
    if not os.path.exists(path):
        raise FileNotFoundError(
            "\n\n"
            "  test_data/search_data.json not found!\n"
            "  Run this command first:\n\n"
            "      python -m ai_generator.generate_test_data\n"
        )
    with open(path, encoding="utf-8") as f:
        return json.load(f)


SEARCH_CASES = _load_cases()


# ─────────────────────────────────────────────────────────────────
# PARAMETRIZED TEST
# One test execution per AI-generated city.
# IDs are the city names for readable pytest output.
# ─────────────────────────────────────────────────────────────────
@pytest.mark.parametrize(
    "case",
    SEARCH_CASES,
    ids=[c["location"] for c in SEARCH_CASES]
)
def test_booking_flow(driver, config, case):
    """
    End-to-end test: Search → Validate Results → Open Hotel → Reserve
    """
    location         = case["location"]
    expected_keyword = case["expected_keyword"]
    description      = case["description"]

    logger.info("=" * 60)
    logger.info(f"TEST START: {description}")
    logger.info(f"Location  : {location}")
    logger.info(f"Keyword   : {expected_keyword}")
    logger.info("=" * 60)

    # ── Step 1: Search for location ───────────────────────────────
    logger.info("Step 1: Entering search location")
    home = HomePage(driver)
    home.search_location(location)

    # ── Step 2: Validate results returned ────────────────────────
    logger.info("Step 2: Validating search results")
    results = ResultsPage(driver)
    count   = results.get_results_count()

    assert count > 0, (
        f"No property cards found for '{location}'. "
        f"Expected at least 1 result but got 0. "
        f"The site layout may have changed or the location is unrecognised."
    )

    logger.info(f"PASS: {count} results found for '{location}'")

    # ── Step 3: Open first hotel detail page ─────────────────────
    logger.info("Step 3: Opening first hotel result")
    results.open_first_result()
    results.switch_to_new_tab()

    # ── Step 4: Click Reserve (Add to Cart equivalent) ────────────
    logger.info("Step 4: Clicking Reserve button")
    hotel = HotelPage(driver)
    hotel.click_reserve()

    logger.info(f"TEST PASSED: {description}")
    logger.info("=" * 60)