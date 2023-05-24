import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import carbonate
from carbonate.exceptions import InvalidXpathException
from test.end2end.webdriver.webdriver_test import WebDriverTest


class failing_test(WebDriverTest):
    def setUp(self):
        self.carbonate_sdk = carbonate.SDK(
            browser=self.browser,
            client=carbonate.Api('test', 'test'),
        )
        self.stubbed_extract_actions = carbonate.Api.extract_actions
        self.stubbed_extract_assertions = carbonate.Api.extract_assertions

        carbonate.Api.extract_actions = lambda *args: []
        carbonate.Api.extract_assertions = lambda *args: []

    def tearDown(self):
        carbonate.Api.extract_actions = self.stubbed_extract_actions
        carbonate.Api.extract_assertions = self.stubbed_extract_assertions

    @carbonate.test()
    def test_it_should_wait_for_renders_to_finish_for_actions(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'type', 'xpath': '//invalidxpath', 'text': 'teststr'}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "render.html"))}')
        self.carbonate_sdk.action('type "teststr" into the input')


if __name__ == "__main__":
    unittest.main()