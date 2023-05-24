import os
import json
from selenium.common import ElementNotInteractableException
from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from .browser import Browser
from .action import Action
from .exceptions import BrowserException


class WebDriver(Browser):
    def __init__(self, driver):
        self.browser = driver
        inject_js_path = os.path.join(os.path.dirname(__file__), "../resources/carbonate.js")
        with open(inject_js_path, "r") as file:
            self.inject_js = file.read()

    def get_html(self):
        return self.browser.execute_script("return document.documentElement.innerHTML")

    def load(self, url, whitelist=None):
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': self.inject_js})

        if whitelist:
            self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': 'window.__set_xhr_whitelist(' + json.dumps(whitelist) + ')'})

        self.browser.get(url)

    def close(self):
        self.browser.quit()

    def get_screenshot(self):
        return self.browser.get_screenshot_as_png()

    def find_by_xpath(self, xpath):
        return self.browser.find_elements(By.XPATH, xpath)

    def find_by_id(self, id):
        return self.browser.find_elements(By.ID, id)

    def evaluate_script(self, script):
        try:
            return self.browser.execute_script(script)
        except JavascriptException as e:
            raise BrowserException("Could not evaluate script: " + script) from e

    def perform_action(self, action, elements):
        if action["action"] == Action.CLICK.value:
            try:
                elements[0].click()
            except ElementNotInteractableException:
                ActionChains(self.browser).move_to_element(elements[0]).click().perform()

        elif action["action"] == Action.TYPE.value:
            if elements[0].tag_name == "label":
                elements = self.find_by_id(elements[0].get_attribute("for"))

            elements[0].send_keys(action["text"])
        elif action["action"] == Action.KEY.value:
            elements[0].send_keys(action["key"])
