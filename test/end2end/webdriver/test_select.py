import os
import unittest
from unittest.mock import Mock

import carbonate_sdk as carbonate
from test.end2end.webdriver.webdriver_test import WebDriverTest


class test_select(WebDriverTest):
    def setUp(self):
        self.api = Mock()
        self.carbonate_sdk = carbonate.SDK(
            browser=self.browser,
            client=self.api,
        )

    @carbonate.test()
    def test_it_should_select_the_option(self):
        self.api.extract_actions.return_value = [{'action': 'click', 'xpath': '//select/option[text()="Two"]'}]
        self.api.extract_assertions.return_value = [{'assertion': "carbonate_assert(document.querySelector('select').value == '2');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')
        self.carbonate_sdk.action('select Two from the dropdown')

        self.assertTrue(self.carbonate_sdk.assertion('the dropdown should be set to Two'))

    @carbonate.test()
    def test_it_should_fail_when_the_assertion_is_wrong(self):
        self.api.extract_actions.return_value = [{'action': 'click', 'xpath': '//select/option[text()="Two"]'}]
        self.api.extract_assertions.return_value = [{'assertion': "carbonate_assert(document.querySelector('select').value == '3');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')
        self.carbonate_sdk.action('select Two from the dropdown')

        self.assertFalse(self.carbonate_sdk.assertion('the dropdown should be set to Three'))

    @carbonate.test()
    def test_it_should_select_the_option_through_the_select(self):
        self.api.extract_actions.return_value = [{'action': 'click', 'xpath': '//select'}, {'action': 'click', 'xpath': '//select/option[text()="Two"]'}]
        self.api.extract_assertions.return_value = [{'assertion': "carbonate_assert(document.querySelector('select').value == '2');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "select.html"))}')
        self.carbonate_sdk.action('select Two from the dropdown')

        self.assertTrue(self.carbonate_sdk.assertion('the dropdown should be set to Two'))

        self.api.extract_actions.assert_called_once()
        self.api.extract_assertions.assert_called_once()

if __name__ == "__main__":
    unittest.main()