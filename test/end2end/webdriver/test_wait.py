import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import carbonate
from carbonate.test_logger import TestLogger
from test.end2end.webdriver.webdriver_test import WebDriverTest


class test_wait(WebDriverTest):
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
    def test_it_should_wait_for_xhr(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('input').value == 'teststr');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_xhr.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should have the contents "teststr"')
        )

    @carbonate.test()
    def test_it_should_wait_for_xhr_for_assertions(self):
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('input').value == '');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_xhr.html"))}')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should be empty')
        )

    @carbonate.test()
    def test_it_should_wait_for_fetch(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('input').value == 'teststr');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_fetch.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should have the contents "teststr"')
        )

    @carbonate.test()
    def test_it_should_wait_for_fetch_for_assertions(self):
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('input').value == '');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_fetch.html"))}')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should be empty')
        )

if __name__ == "__main__":
    unittest.main()