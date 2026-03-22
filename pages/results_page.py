from pages.base_page import BasePage
from locators.results_locators import ResultsLocators
from utils.logger import get_logger

logger = get_logger("ResultsPage")


class ResultsPage(BasePage):

    def get_results_count(self):
        self.wait_for_visible(ResultsLocators.PROPERTY_CARD, timeout=30)
        cards = self.driver.find_elements(*ResultsLocators.PROPERTY_CARD)
        count = len(cards)
        logger.info(f"Property cards found: {count}")
        return count

    def open_first_result(self):
        logger.info("Opening first search result")
        element = self.wait_for_visible(ResultsLocators.FIRST_RESULT, timeout=30)
        self.scroll_into_view(element)
        self.js_click(element)
        logger.info("First result clicked")

    def switch_to_new_tab(self):
        import time
        time.sleep(2)  # wait for new tab to open
        handles = self.driver.window_handles
        if len(handles) > 1:
            self.driver.switch_to.window(handles[1])
            logger.info("Switched to new tab")
        else:
            logger.info("No new tab — staying on current tab")