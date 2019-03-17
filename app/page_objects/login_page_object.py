from app.page_objects.page_object import PageObject


class LoginPageObject(PageObject):
    login_url = "https://www.agilealliance.org/wp-login.php"

    def __init__(self, page_browser, user_login: str, user_password: str):
        super().__init__(page_browser)

        self.user_login = user_login
        self.user_password = user_password

    def login(self):
        self.browser.get(self.login_url)

        self.wait_by_id("user_login")

        user_login = self.browser.find_element_by_id("user_login")
        user_login.clear()
        user_login.send_keys(self.user_login)

        user_login = self.browser.find_element_by_id("user_pass")
        user_login.clear()
        user_login.send_keys(self.user_password)

        submit = self.browser.find_element_by_id("wp-submit")
        submit.click()

        self.wait_by_class_name("navbar-header")
