import pytest
from labra.tasks.web.home_page import HomePageTasks

@pytest.mark.web
@pytest.mark.smoke
def test_homepage_navigation(page, base_config, callsigns):
    home = HomePageTasks(page, base_config, callsigns)

    home.visit_homepage()

@pytest.mark.web
@pytest.mark.smoke
def test_callsign_lookup(page, base_config, callsigns):
    home = HomePageTasks(page, base_config, callsigns)

    home.lookup_callsign()
    home.submit_blank_form()