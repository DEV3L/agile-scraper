from app.page_objects.page_object import PageObject


class LinkedInContactPageObject(PageObject):
    def __init__(self, page_browser, link):
        super().__init__(page_browser)
        self.link = link

    def scrape_contact(self):
        self.browser.get(self.link)

        self.wait_by_id("profile-content")

        dist_value = self.browser.find_element_by_class_name('dist-value')

        if dist_value.text != '1st':
            return

        contact_info_link = self.browser.find_elements_by_xpath("//*[@data-control-name='contact_see_more']")[0]
        contact_info_link.click()

        phone = ''
        email = ''

        try:
            self.wait_by_class_name("ci-email")
            email = self.browser.find_element_by_class_name('ci-email').text
        except Exception as e:
            print("Could not find email address")

        try:
            phone = self.browser.find_element_by_class_name('ci-phone').text
        except Exception as e:
            pass

        return {"phone": phone, "email": email}
