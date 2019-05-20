from app.page_objects.page_object import PageObject


class LinkedInSearchResultsPageObject(PageObject):
    def __init__(self, page_browser):
        super().__init__(page_browser)

    def scrape_contact_links(self):
        self.wait_by_class_name("search-results__total")

        search_results = self.browser.find_elements_by_class_name("search-result--person")
        filtered_search_results = [search_result for search_result in search_results if "1st" in search_result.text]

        contact_links = set()

        for result in filtered_search_results:
            contacts = result.find_elements_by_class_name("search-result__result-link")
            contact_links = {contact.get_property('href') for contact in contacts if contact.get_property('href')}

        return list(contact_links)
