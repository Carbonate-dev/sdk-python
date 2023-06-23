import os
import unittest
from unittest.mock import Mock

import carbonate_sdk as carbonate
from test.end2end.webdriver.webdriver_test import WebDriverTest


class test_whitelist(WebDriverTest):
    def setUp(self):
        self.api = Mock()
        self.carbonate_sdk = carbonate.SDK(
            browser=self.browser,
            client=self.api,
        )

    @carbonate.test()
    def test_it_should_not_wait_for_whitelisted_xhr(self):
        self.api.extract_actions.return_value = [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]
        self.api.extract_assertions.return_value = [{'assertion': "carbonate_assert(document.querySelector('input').value == 'teststr');"}]

        self.carbonate_sdk.whitelist_network('https://api.staging.carbonate.dev/internal/test_wait*')

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "whitelist_xhr.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should have the contents "teststr"')
        )

        self.api.extract_actions.assert_called_once()
        self.api.extract_assertions.assert_called_once()

    @carbonate.test()
    def test_it_should_not_wait_for_whitelisted_fetch(self):
        self.api.extract_actions.return_value = [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]
        self.api.extract_assertions.return_value = [{'assertion': "carbonate_assert(document.querySelector('input').value == 'teststr');"}]

        self.carbonate_sdk.whitelist_network('https://api.staging.carbonate.dev/internal/test_wait*')
        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "whitelist_fetch.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should have the contents "teststr"')
        )

        self.api.extract_actions.assert_called_once()
        self.api.extract_assertions.assert_called_once()

if __name__ == "__main__":
    unittest.main()