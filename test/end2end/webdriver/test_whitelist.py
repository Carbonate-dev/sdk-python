import os
import unittest
import carbonate
from test.end2end.webdriver.webdriver_test import WebDriverTest


class test_whitelist(WebDriverTest):
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
    def test_it_should_not_wait_for_whitelisted_xhr(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('input').value == 'teststr');"}]

        self.carbonate_sdk.whitelistNetwork('https://api.staging.carbonate.dev/internal/test_wait*')

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "whitelist_xhr.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should have the contents "teststr"')
        )

    @carbonate.test()
    def test_it_should_not_wait_for_whitelisted_fetch(self):
        carbonate.Api.extract_actions = lambda *args: [{'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]
        carbonate.Api.extract_assertions = lambda *args: [{'assertion': "assert(document.querySelector('input').value == 'teststr');"}]

        self.carbonate_sdk.whitelistNetwork('https://api.staging.carbonate.dev/internal/test_wait*')
        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "whitelist_fetch.html"))}')

        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.assertion('the input should have the contents "teststr"')
        )

if __name__ == "__main__":
    unittest.main()