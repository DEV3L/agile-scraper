import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

user_password = os.environ['USER_PASS']


class PageObject:
    def __init__(self, browser):
        self.browser = browser

    def wait_by_id(self, element_id):
        WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((By.ID, element_id)))


class LoginPageObject(PageObject):
    login_url = "https://www.agilealliance.org/wp-login.php"

    def login(self):
        self.browser.get(self.login_url)

        self.wait_by_id("user_login")

        user_login = self.browser.find_element_by_id("user_login")
        user_login.clear()
        user_login.send_keys("jus.beall@gmail.com")

        user_login = self.browser.find_element_by_id("user_pass")
        user_login.clear()
        user_login.send_keys(user_password)

        submit = self.browser.find_element_by_id("wp-submit")
        submit.click()


class SessionPageObject(PageObject):
    session_page = "https://submissions.agilealliance.org/agile2019/sessions/10558"

    def print_page(self):
        self.browser.get(self.session_page)

        print(BeautifulSoup(browser.page_source).text)


if __name__ == '__main__':
    browser = webdriver.Chrome()

    login_page = LoginPageObject(browser)
    login_page.login()

    session_page = SessionPageObject(browser)
    session_page.print_page()

    browser.close()
