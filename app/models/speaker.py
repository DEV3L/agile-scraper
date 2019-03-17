from app.models.model import Model
from selenium.webdriver.remote.webelement import WebElement


class Speaker(Model):
    def __init__(self, ):
        self._id = ''
        self.url = ''
        self.speaker_name = ''

    def from_web_element(self, web_element: WebElement):
        self.url = web_element.get_attribute('href')
        self.speaker_name = web_element.text
