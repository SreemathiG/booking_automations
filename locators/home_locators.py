from selenium.webdriver.common.by import By


class HomeLocators:
    SEARCH_BOX    = (By.NAME, "ss")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SIGNIN_CLOSE  = (By.XPATH, "//button[@aria-label='Dismiss sign-in info.']")
    COOKIE_ACCEPT = (By.ID, "onetrust-accept-btn-handler")