import os
import unittest
from unittest.mock import Mock

import carbonate_sdk as carbonate
from test.end2end.webdriver.webdriver_test import WebDriverTest


class test_wait_cached(WebDriverTest):
    def setUp(self):
        self.api = Mock()
        self.carbonate_sdk = carbonate.SDK(
            cache_dir=os.path.join(os.path.splitext(__file__)[0]),
            browser=self.browser,
            client=self.api,
        )

    @carbonate.test()
    def test_it_should_wait_for_xhr_before_performing_actions(self):
        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_xhr.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.browser.evaluate_script("return document.querySelector('input').value == 'teststr'")
        )

        self.assertIn(
            'Waiting for active Network to finish',
            self.carbonate_sdk.get_logger().get_logs()
        )

        self.api.extract_actions.assert_not_called()

    @carbonate.test()
    def test_it_should_wait_for_xhr_before_performing_assertions(self):
        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_xhr.html"))}')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should be empty')
        )

        self.assertIn(
            'Waiting for active Network to finish',
            self.carbonate_sdk.get_logger().get_logs()
        )

        self.api.extract_assertions.assert_not_called()

    @carbonate.test()
    def test_it_should_wait_for_fetch_before_performing_actions(self):
        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_fetch.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.browser.evaluate_script("return document.querySelector('input').value == 'teststr'")
        )

        self.assertIn(
            'Waiting for active Network to finish',
            self.carbonate_sdk.get_logger().get_logs()
        )

        self.api.extract_actions.assert_not_called()

    @carbonate.test()
    def test_it_should_wait_for_fetch_before_performing_assertions(self):
        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "wait_fetch.html"))}')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should be empty')
        )

        self.assertIn(
            'Waiting for active Network to finish',
            self.carbonate_sdk.get_logger().get_logs()
        )

        self.api.extract_assertions.assert_not_called()


if __name__ == "__main__":
    unittest.main()