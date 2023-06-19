import os
import unittest
from unittest.mock import Mock

import carbonate
from carbonate.exceptions import InvalidXpathException
from test.end2end.webdriver.webdriver_test import WebDriverTest


class test_notfound(WebDriverTest):
    def setUp(self):
        self.api = Mock()
        self.carbonate_sdk = carbonate.SDK(
            browser=self.browser,
            client=self.api,
        )

    @carbonate.test()
    def test_it_should_error_if_xpath_is_not_found_for_an_action(self):
        self.api.extract_actions.return_value = [{'action': 'click', 'xpath': '//select//option[text()=\'Birthday\']', 'text': None}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')

        self.assertRaises(
            InvalidXpathException,
            self.carbonate_sdk.action,
            'chose Birthday as the event type'
        )

    @carbonate.test()
    def test_it_should_error_if_xpath_is_not_found_for_a_lookup(self):
        self.api.extract_lookup.return_value = {'xpath': '//select//option[text()=\'Birthday\']'}

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')

        self.assertRaises(
            InvalidXpathException,
            self.carbonate_sdk.lookup,
            'the event type dropdown'
        )

if __name__ == "__main__":
    unittest.main()