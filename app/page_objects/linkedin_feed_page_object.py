from selenium.webdriver.common.keys import Keys

from app.page_objects.page_object import PageObject


class LinkedInFeedPageObject(PageObject):
    def __init__(self, page_browser):
        super().__init__(page_browser)

    def search_contact(self, contact):
        self.browser.get('https://www.linkedin.com/feed/')

        self.wait_by_class_name("lazy-image")

        search_input = self.browser.find_elements_by_xpath("//*[@placeholder='Search']")[0]
        search_input.clear()
        search_input.send_keys(f'{contact.first_name} {contact.last_name}')
        search_input.send_keys(Keys.ENTER)

        try:
            self.wait_by_class_name("search-results__total")
        except Exception as e:
            print('Could not find results for contact')
            return False

        return True

    def search(self, search_value: str):
        self.browser.get('https://www.linkedin.com/feed/')

        self.wait_by_class_name("lazy-image")

        search_input = self.browser.find_elements_by_xpath("//*[@placeholder='Search']")[0]
        search_input.clear()
        search_input.send_keys(f'{search_value}')
        search_input.send_keys(Keys.ENTER)

        try:
            self.wait_by_class_name("search-results__total")
        except Exception as e:
            print('Could not find results for contact')
            return False

        return True
