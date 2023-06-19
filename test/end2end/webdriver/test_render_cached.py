import os
import unittest
from unittest.mock import Mock

import carbonate
from carbonate.exceptions import InvalidXpathException
from test.end2end.webdriver.test_render import test_render
from test.end2end.webdriver.webdriver_test import WebDriverTest

class test_render_cached(WebDriverTest):
    def setUp(self):
        self.api = Mock()
        self.carbonate_sdk = carbonate.SDK(
            cache_dir=os.path.join(os.path.splitext(__file__)[0]),
            browser=self.browser,
            client=self.api,
        )

    @carbonate.test()
    def test_it_should_wait_for_renders_to_finish_for_actions(self):
        self.api.extract_actions.return_value = [
            {'action': 'type', 'xpath': '//label[@for="input"]', 'text': 'teststr'}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "render.html"))}')
        self.carbonate_sdk.action('type "teststr" into the input')

        self.assertTrue(
            self.carbonate_sdk.browser.evaluate_script("return document.querySelector('input').value == 'teststr'")
        )

        self.assertIn(
            'Waiting for DOM update to finish',
            self.carbonate_sdk.get_logger().get_logs()
        )

        self.api.extract_actions.assert_not_called()

    @carbonate.test()
    def test_it_should_wait_for_renders_to_finish_for_assertions(self):
        self.api.extract_assertions.return_value = [
            {'assertion': "carbonate_assert(document.querySelector('label').innerText == 'Test');"}]

        self.carbonate_sdk.load(f'file:///{os.path.abspath(os.path.join(".", "test", "fixtures", "render.html"))}')

        self.assertTrue(self.carbonate_sdk.assertion('there should be a label with the text "test"'))

        self.api.extract_assertions.assert_not_called()


if __name__ == "__main__":
    unittest.main()