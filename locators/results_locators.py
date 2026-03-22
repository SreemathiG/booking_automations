from selenium.webdriver.common.by import By


class ResultsLocators:
    PROPERTY_CARD = (By.CSS_SELECTOR, "[data-testid='property-card']")
    FIRST_RESULT  = (By.CSS_SELECTOR, "[data-testid='property-card'] a")