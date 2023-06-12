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


class test_select(WebDriverTest):
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
    def test_select_by_option(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'click', 'xpath': '//select/option[text()="Two"]'}]
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('select').value == '2');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')
        self.carbonate_sdk.action('select Two from the dropdown')

        self.assertTrue(self.carbonate_sdk.assertion('the dropdown should be set to Two'))

    @carbonate.test()
    def test_select_by_option_not_successful(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'click', 'xpath': '//select/option[text()="Two"]'}]
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('select').value == '3');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')
        self.carbonate_sdk.action('select Two from the dropdown')

        self.assertFalse(self.carbonate_sdk.assertion('the dropdown should be set to Three'))

    @carbonate.test()
    def test_select_option_through_select(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'click', 'xpath': '//select'}]
        carbonate.Api.extract_actions = lambda *args: [{'action': 'click', 'xpath': '//select/option[text()="Two"]'}]
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('select').value == '2');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')
        self.carbonate_sdk.action('select Two from the dropdown')

        self.assertTrue(self.carbonate_sdk.assertion('the dropdown should be set to Two'))

    @carbonate.test()
    def test_label_for(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('input').value == 'teststr');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "label.html"))}')
        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(self.carbonate_sdk.assertion('the input should have the contents "teststr"'))

if __name__ == "__main__":
    unittest.main()