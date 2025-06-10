from playwright.sync_api import sync_playwright

class WebDriver(BaseDriver):
    def setup(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def execute(self, actions: list):
        for action in actions:
            method = getattr(self.page, action["method"])
            method(*action["args"], **action["kwargs"])

    def teardown(self):
        self.browser.close()
        self.playwright.stop()
