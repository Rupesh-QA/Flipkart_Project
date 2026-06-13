import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_instance():
    """Reuse single browser for all tests"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        yield browser
        browser.close()


@pytest.fixture
def page(browser_instance):
    """Create new page for each test with isolated state"""
    context = browser_instance.new_context()
    page = context.new_page()

    yield page

    
    try:
        page.wait_for_timeout(3000)
    except Exception:
        pass


    try:
        page.evaluate("window.localStorage.clear()")
        page.evaluate("window.sessionStorage.clear()")
    except Exception:
        pass
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_path = f"failure_{item.name}.png"
            try:
                page.screenshot(path=screenshot_path)
                print(f"\nSaved failure screenshot to {screenshot_path}")
            except Exception as e:
                print(f"\nFailed to save screenshot: {e}")

