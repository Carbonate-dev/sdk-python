import json
import os
import time
import unittest
from unittest.mock import Mock

import carbonate_sdk as carbonate
from test.end2end.webdriver.webdriver_test import WebDriverTest
from unittest_data_provider import data_provider  # type: ignore

class test_input(WebDriverTest):
    def setUp(self):
        self.api = Mock()
        self.carbonate_sdk = carbonate.SDK(
            browser=self.browser,
            client=self.api,
        )

    inputAndDateDataProvider = lambda: (
        ['color', '//input[@id="color"]', '#ff0000'],
        ['email', '//input[@id="email"]', 'test@example.org'],
        ['number', '//input[@id="number"]', '12'],
        ['password', '//input[@id="password"]', 'teststr'],
        ['range', '//input[@id="range"]', '50'],
        ['search', '//input[@id="search"]', 'teststr'],
        ['tel', '//input[@id="tel"]', '01234567890'],
        ['text', '//input[@id="text"]', 'teststr'],
        ['url', '//input[@id="url"]', 'http://example.org'],
        ['textarea', '//textarea[@id="textarea"]', "This\nis\na\ntest"],
        ['date', '//input[@id="date"]', '2022-01-01'],
        ['datetime-local', '//input[@id="datetime-local"]', '2022-01-01T00:00'],
        ['month', '//input[@id="month"]', '2022-01'],
        ['time', '//input[@id="time"]', '00:00:00'],
        ['week', '//input[@id="week"]', '2022-W01'],
    )

    checkDataProvider = lambda: (
        ['radio', '//input[@id="radio"]', '1'],
        ['checkbox', '//input[@id="checkbox"]', '1'],
    )

    @data_provider(inputAndDateDataProvider)
    @carbonate.test()
    def test_it_should_fill_in_the_input(self, name, xpath, value):
        self.api.reset_mock()

        self.api.extract_actions.return_value = [{'action': 'type', 'xpath': xpath, 'text': value}]
        self.api.extract_assertions.return_value = [{'assertion': f"carbonate_assert(document.querySelector('#{name}').value == {json.dumps(value)});"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "input.html"))}')
        self.carbonate_sdk.action(f'type "f{value}" into the f{name} input')

        self.assertTrue(self.carbonate_sdk.assertion(f'the {name} input should have the contents "{value}"'))

        self.assertTrue(self.carbonate_sdk.get_browser().evaluate_script(f"return window.hasChanged['{name}']"))

        self.api.extract_actions.assert_called_once()
        self.api.extract_assertions.assert_called_once()

    @data_provider(checkDataProvider)
    @carbonate.test()
    def test_it_should_click_the_element(self, name, xpath, value):
        self.api.reset_mock()

        self.api.extract_actions.return_value = [{'action': 'click', 'xpath': xpath}]
        self.api.extract_assertions.return_value = [{'assertion': f"carbonate_assert(document.querySelector('#{name}').value == {json.dumps(value)});"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "input.html"))}')
        self.carbonate_sdk.action(f'click the f{name} element')

        self.assertTrue(self.carbonate_sdk.assertion(f'the {name} element should have the value "{value}"'))

        self.assertTrue(self.carbonate_sdk.get_browser().evaluate_script(f"return window.hasChanged['{name}']"))

        self.api.extract_actions.assert_called_once()
        self.api.extract_assertions.assert_called_once()

    @carbonate.test()
    def test_it_should_fill_in_an_input_when_given_a_label(self):
        self.api.extract_actions.return_value = [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]
        self.api.extract_assertions.return_value = [{'assertion': "carbonate_assert(document.querySelector('input').value == 'teststr');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "label.html"))}')
        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(self.carbonate_sdk.assertion('the input should have the contents "teststr"'))

        self.api.extract_actions.assert_called_once()
        self.api.extract_assertions.assert_called_once()

if __name__ == "__main__":
    unittest.main()