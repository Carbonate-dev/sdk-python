import os
import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import carbonate_sdk as carbonate


class WebDriverTest(unittest.TestCase):
    browser = None

    @classmethod
    def setUpClass(cls) -> None:
        chrome_path = os.getenv('CHROME_PATH')

        if not chrome_path:
            chrome_path = ChromeDriverManager().install()

        chrome_options = Options()
        options = [
            "--headless",
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        for option in options:
            chrome_options.add_argument(option)

        driver = webdriver.Chrome(service=Service(executable_path=chrome_path), options=chrome_options)
        cls.browser = carbonate.WebDriver(driver)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()

if __name__ == "__main__":
    unittest.main()