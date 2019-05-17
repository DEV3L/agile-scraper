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

        self.wait_by_class_name("search-results__total")
