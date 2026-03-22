import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from locators.home_locators import HomeLocators
from utils.logger import get_logger

logger = get_logger("HomePage")

AUTOCOMPLETE_FIRST = (By.CSS_SELECTOR, "li[id='autocomplete-result-0']")


class HomePage(BasePage):

    def _safe_dismiss(self, locator, label):
        if self.is_visible(locator, timeout=5):
            try:
                element = self.wait_for_visible(locator)
                self.js_click(element)
                logger.info(f"Dismissed: {label}")
            except Exception as e:
                logger.info(f"Could not dismiss '{label}': {e}")

    def close_popups(self):
        self._safe_dismiss(HomeLocators.SIGNIN_CLOSE, "sign-in banner")
        self._safe_dismiss(HomeLocators.COOKIE_ACCEPT, "cookie banner")

    def search_location(self, location):
        logger.info(f"Searching for: '{location}'")

        # Step 1: Dismiss popups
        self.close_popups()

        # Step 2: Wait longer for page load then type location
        search_box = self.wait_for_visible(HomeLocators.SEARCH_BOX, timeout=30)
        search_box.clear()
        search_box.send_keys(location)
        logger.info("Location typed into search box")

        # Step 3: Wait for autocomplete then JS click first result
        time.sleep(1.5)
        try:
            elements = self.driver.find_elements(*AUTOCOMPLETE_FIRST)
            if elements:
                self.driver.execute_script("arguments[0].click();", elements[0])
                logger.info("Autocomplete first result clicked via JS")
            else:
                search_box.send_keys(Keys.RETURN)
                logger.info("No autocomplete — pressed Enter")
        except Exception as e:
            logger.info(f"Autocomplete fallback to Enter: {e}")
            search_box.send_keys(Keys.RETURN)

        # Step 4: Click search button via JS
        time.sleep(0.5)
        try:
            btn = self.wait_for_visible(HomeLocators.SEARCH_BUTTON, timeout=15)
            self.driver.execute_script("arguments[0].click();", btn)
            logger.info("Search button clicked via JS")
        except Exception as e:
            logger.error(f"Search button failed: {e}")
            raise