from app.page_objects.page_object import PageObject


class LinkedInSearchResultsPageObject(PageObject):
    def __init__(self, page_browser):
        super().__init__(page_browser)

    def scrape_contact_links(self):
        self.wait_by_class_name("search-results__total")

        contacts = self.browser.find_elements_by_class_name("search-result__result-link")

        contact_links = {contact.get_property('href') for contact in contacts if contact.get_property('href')}

        return list(contact_links)
