from app.page_objects.page_object import PageObject


class LinkedInLoginPageObject(PageObject):
    login_url = "https://www.linkedin.com/login"

    def __init__(self, page_browser, user_login: str, user_password: str):
        super().__init__(page_browser)

        self.user_login = user_login
        self.user_password = user_password

    def login(self):
        self.browser.get(self.login_url)

        self.wait_by_id("username")

        user_login = self.browser.find_element_by_id("username")
        user_login.clear()
        user_login.send_keys(self.user_login)

        user_login = self.browser.find_element_by_id("password")
        user_login.clear()
        user_login.send_keys(self.user_password)

        submit = self.browser.find_element_by_class_name("btn__primary--large")
        submit.click()

        self.wait_by_class_name("lazy-image")
