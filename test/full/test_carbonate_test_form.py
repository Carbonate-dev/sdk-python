import carbonate_sdk as carbonate
from selenium.webdriver.support.select import Select
from test.end2end.webdriver.webdriver_test import WebDriverTest

class test_carbonate_test_form(WebDriverTest):
    def setUp(self):
        self.carbonate_sdk = carbonate.SDK(
            browser=self.browser,
        )

    @carbonate.test()
    def test_birthday_event_type(self):
        self.carbonate_sdk.load(
            # 'https://carbonate.dev/demo-form',
            'https://testbot-website.vercel.app/demo-form'
        )

        self.carbonate_sdk.action('chose Birthday as the event type')

        self.assertTrue(
            self.carbonate_sdk.assertion('the event type should be Birthday')
        )

        self.assertEqual(
            'Birthday',
            Select(self.carbonate_sdk.lookup('the event type dropdown')).first_selected_option.text
        )

