# src/labra/action/web_tasks.py
from playwright.sync_api import Page

class HomePageTasks:

    def __init__(self, page: Page, base_config, callsigns):
        self.page = page
        self.base_url = base_config["base_url"]
        self.callsigns = callsigns

    def lookup_callsign(self):
        test_data = self.callsigns["VALID"]
        callsign = test_data['callsign']

        self.page.goto(url=self.base_url)
        self.page.click("input[id='callsign']")
        self.page.fill("input[name='callsign']", callsign)
        self.page.press("input[name='callsign']", "Enter")
        self.page.wait_for_url(f"{self.base_url}{callsign}")
        assert callsign in self.page.url

    def visit_homepage(self):

        self.page.goto(url=self.base_url)
        assert "ham radio" in self.page.content()

    def submit_blank_form(self):

        self.page.goto(url=self.base_url)
        self.page.click("input[name='callsign']")
        self.page.press("input[name='callsign']", "Enter")
        self.page.wait_for_timeout(3000)
        assert self.page.url == self.base_url, f"Submit not redirected to home! Got {self.page.url} instead."
