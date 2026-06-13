from playwright.sync_api import expect
from .base_page import BasePage
from utils.config import BASE_URL


class HomePage(BasePage):

    HOMEPAGE_URL = BASE_URL

    def __init__(self, page):

        super().__init__(page)

    @property
    def logo(self):

        return self.page.locator("a[href='https://www.flipkart.com/']:visible, a[href='/']:visible").first

    @property
    def search_bar(self):

        return self.page.locator("input[placeholder*='Search']").first

    @property
    def search_button(self):

        return self.page.locator("button[type='submit']").first

    @property
    def product_titles(self):

        return self.page.locator("div[data-id]")

    @property
    def search_suggestions(self):

        return self.page.locator("li")

    def open_homepage(self):

        self.page.goto(self.HOMEPAGE_URL)

        self.close_login_popup()

    def enter_search_text(self, text):

        self.search_bar.fill(text)

    def search_product(self, product_name):

        self.search_bar.wait_for(state="visible", timeout=5000)

        self.search_bar.fill(product_name)

        self.search_button.click()

        expect(self.product_titles.first).to_be_visible()