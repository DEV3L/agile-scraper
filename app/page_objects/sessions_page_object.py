from app.models.session import Session
from app.models.speaker import Speaker
from app.page_objects.page_object import PageObject


class SessionPageObject(PageObject):
    def __init__(self, page_browser, session_dao, speaker_dao):
        super().__init__(page_browser)
        self.session_dao = session_dao
        self.speaker_dao = speaker_dao

    def scrape_session(self, session_page):
        self.browser.get(session_page)

        speakers = self.speaker_dao.find_all()
        speakers_by_name = {speaker['speaker_name']: speaker for speaker in speakers}

        sessions = self.session_dao.find_all()
        sessions_by_session_id = {session['session_id']: session for session in sessions}

        self.wait_by_class_name("session")

        sessions = self.browser.find_elements_by_class_name("session")

        for session_element in sessions:
            session = Session()
            session.from_web_element(session_element)

            if session.session_id not in sessions_by_session_id:
                _id = self.session_dao.create(session)
                session._id = _id
                sessions_by_session_id[session.session_id] = session

        speaker_elements = self.browser.find_elements_by_xpath("//*[@data-modal='user_profile']")

        for speaker_element in speaker_elements:
            speaker = Speaker()
            speaker.from_web_element(speaker_element)

            if speaker.speaker_name not in speakers_by_name:
                _id = self.speaker_dao.create(speaker)
                speaker._id = _id
                speakers_by_name[speaker.speaker_name] = speaker

        return len(sessions)
