import os

from app.daos.mongo import MongoDatabase
from app.daos.speaker_dao import SpeakerDao
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

    def __init__(self, page_browser, speaker_dao):
        super().__init__(page_browser)
        self.speaker_dao = speaker_dao

    def scrape_session(self):
        self.browser.get(self.session_page)

        speakers = self.speaker_dao.find_all()
        speakers_by_name = {speaker['speaker_name']: speaker for speaker in speakers}

        self.wait_by_class_name("session")

        sessions = self.browser.find_elements_by_class_name("session")

        for session in sessions:
            session_text = session.text
            session_tokens = session_text.split(' ')

            status = session_tokens[0]
            session_id = session_tokens[1]
            session_name = session.find_element_by_class_name('title').text
            url = session.get_attribute('data-vote-url')

            speaker_text = " ".join(session_tokens[2:-3])
            speaker_text = speaker_text.replace(session_name, '')
            speaker_text = speaker_text.replace('about', '').strip()

            print()


        speaker_elements = self.browser.find_elements_by_xpath("//*[@data-modal='user_profile']")

        for speaker_element in speaker_elements:
            speaker = Speaker()
            speaker.from_web_element(speaker_element)

            if speaker.speaker_name not in speakers_by_name:
                _id = self.speaker_dao.create(speaker)
                speaker._id = _id
                speakers_by_name[speaker.speaker_name] = speaker


if __name__ == '__main__':
    # DAOs
    _speaker_dao = SpeakerDao(MongoDatabase())

    # Selenium
    browser = webdriver.Chrome()

    login_page = LoginPageObject(browser, user_login_value, user_password_value)
    login_page.login()

    session_page = SessionPageObject(browser, _speaker_dao)
    session_page.scrape_session()

    browser.close()
