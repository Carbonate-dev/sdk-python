import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import carbonate
from carbonate.test_logger import TestLogger


class WebDriverTest(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        chrome_path = os.getenv('CHROME_PATH')

        if not chrome_path:
            chrome_path = ChromeDriverManager().install()

        chrome_options = Options()
        options = [
            # "--headless",
            "--disable-gpu",
            "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        for option in options:
            chrome_options.add_argument(option)

        driver = webdriver.Chrome(chrome_path, options=chrome_options)
        self.browser = carbonate.WebDriver(driver)

if __name__ == "__main__":
    unittest.main()