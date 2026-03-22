from pages.base_page import BasePage
from locators.hotel_locators import HotelLocators
from utils.logger import get_logger

logger = get_logger("HotelPage")


class HotelPage(BasePage):

    def click_reserve(self):
        logger.info("Waiting for Reserve button")
        self.click(HotelLocators.RESERVE_BUTTON)
        logger.info("Reserve button clicked successfully")