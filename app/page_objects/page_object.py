from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class PageObject:
    def __init__(self, page_browser):
        self.browser = page_browser

    def wait_by_id(self, element_id):
        WebDriverWait(self.browser, 3).until(expected_conditions.presence_of_element_located((By.ID, element_id)))

    def wait_by_class_name(self, class_name):
        WebDriverWait(self.browser, 5).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, class_name)))
