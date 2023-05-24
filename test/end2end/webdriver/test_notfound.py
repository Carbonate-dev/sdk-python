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


class test_notfound(WebDriverTest):
    def setUp(self):
        self.carbonate_sdk = carbonate.SDK(
            browser=self.browser,
            client=carbonate.Api('test', 'test'),
        )
        self.stubbed_extract_actions = carbonate.Api.extract_actions
        self.stubbed_extract_assertions = carbonate.Api.extract_assertions
        self.stubbed_extract_lookup = carbonate.Api.extract_lookup

        carbonate.Api.extract_actions = lambda *args: []
        carbonate.Api.extract_assertions = lambda *args: []
        carbonate.Api.extract_lookup = lambda *args: []

    def tearDown(self):
        carbonate.Api.extract_actions = self.stubbed_extract_actions
        carbonate.Api.extract_assertions = self.stubbed_extract_assertions
        carbonate.Api.extract_lookup = self.stubbed_extract_lookup

    @carbonate.test()
    def test_it_should_error_if_xpath_is_not_found_for_an_action(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'click', 'xpath': '//select//option[text()=\'Birthday\']', 'text': None}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')

        self.assertRaises(
            InvalidXpathException,
            self.carbonate_sdk.action,
            'chose Birthday as the event type'
        )

    @carbonate.test()
    def test_it_should_error_if_xpath_is_not_found_for_a_lookup(self):
        carbonate.Api.extract_lookup = lambda *args: {'xpath': '//select//option[text()=\'Birthday\']'}

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')

        self.assertRaises(
            InvalidXpathException,
            self.carbonate_sdk.lookup,
            'the event type dropdown'
        )

if __name__ == "__main__":
    unittest.main()