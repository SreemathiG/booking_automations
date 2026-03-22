from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:

    def __init__(self, driver, timeout=15):
        self.driver  = driver
        self.timeout = timeout

    def wait_for_visible(self, locator, timeout=None):
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator, timeout=None):
        t = timeout if timeout is not None else self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator, timeout=None):
        self.wait_for_clickable(locator, timeout).click()

    def type(self, locator, text, timeout=None):
        element = self.wait_for_visible(locator, timeout)
        element.clear()
        element.send_keys(text)

    def is_visible(self, locator, timeout=4):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def get_current_url(self):
        return self.driver.current_url