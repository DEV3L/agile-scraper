import os

from app.models.speaker import Speaker
from app.page_objects.login_page_object import LoginPageObject
from app.page_objects.page_object import PageObject
from environs import Env
from selenium import webdriver

Env().read_env(path="./.env")

user_login_value = os.environ['USER_LOGIN']
user_password_value = os.environ['USER_PASS']


class SessionPageObject(PageObject):
    session_page = "https://submissions.agilealliance.org/agile2019/sessions?page=1"

    def scrape_session(self):
        self.browser.get(self.session_page)

        self.wait_by_class_name("session")

        sessions = self.browser.find_elements_by_class_name("session")

        for session in sessions:
            url = session.get_attribute('data-vote-url')
            print(url)

        speaker_elements = self.browser.find_elements_by_xpath("//*[@data-modal='user_profile']")
        speakers = []

        for speaker_element in speaker_elements:
            speaker = Speaker()
            speaker.from_web_element(speaker_element)
            print(speaker)
            speakers.append(speaker)


if __name__ == '__main__':
    browser = webdriver.Chrome()

    login_page = LoginPageObject(browser, user_login_value, user_password_value)
    login_page.login()

    session_page = SessionPageObject(browser)
    session_page.scrape_session()

    browser.close()
