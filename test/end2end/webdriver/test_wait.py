import os
import unittest
from unittest.mock import Mock

import carbonate_sdk as carbonate
from test.end2end.webdriver.webdriver_test import WebDriverTest


class test_wait(WebDriverTest):
    def setUp(self):
        self.api = Mock()
        self.carbonate_sdk = carbonate.SDK(
            browser=self.browser,
            client=self.api,
        )

    @carbonate.test()
    def test_it_should_wait_for_xhr_before_performing_actions(self):
        self.api.extract_actions.return_value = [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_xhr.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.browser.evaluate_script("return document.querySelector('input').value == 'teststr'")
        )

        self.assertIn(
            'Waiting for active Network to finish',
            self.carbonate_sdk.get_logger().get_logs()
        )

        self.api.extract_actions.assert_called_once()

    @carbonate.test()
    def test_it_should_wait_for_xhr_before_performing_assertions(self):
        self.api.extract_assertions.return_value = [{'assertion': "carbonate_assert(document.querySelector('input').value == '');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_xhr.html"))}')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should be empty')
        )

        self.assertIn(
            'Waiting for active Network to finish',
            self.carbonate_sdk.get_logger().get_logs()
        )

        self.api.extract_assertions.assert_called_once()

    @carbonate.test()
    def test_it_should_wait_for_fetch_before_performing_actions(self):
        self.api.extract_actions.return_value = [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_fetch.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.browser.evaluate_script("return document.querySelector('input').value == 'teststr'")
        )

        self.assertIn(
            'Waiting for active Network to finish',
            self.carbonate_sdk.get_logger().get_logs()
        )

        self.api.extract_actions.assert_called_once()

    @carbonate.test()
    def test_it_should_wait_for_fetch_before_performing_assertions(self):
        self.api.extract_assertions.return_value = [{'assertion': "carbonate_assert(document.querySelector('input').value == '');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_fetch.html"))}')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should be empty')
        )

        self.assertIn(
            'Waiting for active Network to finish',
            self.carbonate_sdk.get_logger().get_logs()
        )

        self.api.extract_assertions.assert_called_once()

if __name__ == "__main__":
    unittest.main()