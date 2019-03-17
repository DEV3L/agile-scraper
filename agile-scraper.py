import os

from app.daos.mongo import MongoDatabase
from app.daos.session_dao import SessionDao
from app.daos.speaker_dao import SpeakerDao
from app.page_objects.login_page_object import LoginPageObject
from app.page_objects.sessions_page_object import SessionPageObject
from environs import Env
from selenium import webdriver

Env().read_env(path="./.env")

user_login_value = os.environ['USER_LOGIN']
user_password_value = os.environ['USER_PASS']


if __name__ == '__main__':
    _session_dao = SessionDao(MongoDatabase())
    _speaker_dao = SpeakerDao(MongoDatabase())

    browser = webdriver.Chrome()

    login_page = LoginPageObject(browser, user_login_value, user_password_value)
    login_page.login()

    session_page = SessionPageObject(browser, _session_dao, _speaker_dao)

    page_number = 0
    sessions_count = 1

    while sessions_count:
        page_number += 1
        _session_page = f'https://submissions.agilealliance.org/agile2019/sessions?page={page_number}'
        sessions_count = session_page.scrape_session(_session_page)

    browser.close()
    # 1945 sessions, 1321 speakers
