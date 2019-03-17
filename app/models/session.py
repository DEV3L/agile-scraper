from app.models.model import Model
from selenium.webdriver.remote.webelement import WebElement


class Session(Model):
    def __init__(self):
        self._id = ''
        self.url = ''
        self.status = ''
        self.session_id = ''
        self.session_name = ''
        self.speaker_text = ''

    def from_web_element(self, web_element: WebElement):
        session_text = web_element.text
        session_tokens = session_text.split(' ')

        self.status = session_tokens[0]
        self.session_id = session_tokens[1]
        self.session_name = web_element.find_element_by_class_name('title').text
        self.url = web_element.get_attribute('data-vote-url').replace('/vote', '')

        speaker_text = " ".join(session_tokens[2:-3])
        speaker_text = speaker_text.replace(session_name, '')
        speaker_text = speaker_text.replace('about', '').strip()
        self.speaker_text = speaker_text
