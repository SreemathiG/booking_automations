import os
from datetime import datetime
from utils.logger import get_logger

logger = get_logger("Screenshot")


def take_screenshot(driver, test_name):
    """
    Captures a screenshot and saves it under reports/screenshots/.
    Automatically called by conftest.py whenever a test fails.

    File naming: <test_name>_<timestamp>.png
    Special characters in test_name are sanitized for safe filenames.
    """
    try:
        folder = os.path.join("reports", "screenshots")
        os.makedirs(folder, exist_ok=True)

        # Sanitize test name for use as filename
        safe_name = (
            test_name
            .replace("[", "_")
            .replace("]", "_")
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(folder, f"{safe_name}_{timestamp}.png")

        driver.save_screenshot(file_path)
        logger.info(f"Screenshot saved: {file_path}")
        print(f"\n  Screenshot saved: {file_path}")

    except Exception as e:
        logger.error(f"Failed to capture screenshot for '{test_name}': {e}")