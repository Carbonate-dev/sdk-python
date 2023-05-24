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
from test.end2end.webdriver.test_render import test_render
from test.end2end.webdriver.webdriver_test import WebDriverTest

class test_render_cached(test_render):
    def setUp(self):
        self.carbonate_sdk = carbonate.SDK(
            cache_dir=os.path.join(os.path.splitext(__file__)[0]),
            browser=self.browser,
            client=carbonate.Api('test', 'test'),
        )
        self.stubbed_extract_actions = carbonate.Api.extract_actions
        self.stubbed_extract_assertions = carbonate.Api.extract_assertions

        carbonate.Api.extract_actions = self.raise_should_not_be_called
        carbonate.Api.extract_assertions = self.raise_should_not_be_called

    def raise_should_not_be_called(self):
        raise "This should not be called"

if __name__ == "__main__":
    unittest.main()