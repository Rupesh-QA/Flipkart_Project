class BasePage:
    def __init__(self, page):
        self.page = page

    def goto_url(self, url):
        self.page.goto(url)

    def close_login_popup(self):
        """Close the Flipkart login popup when it appears."""
        self.page.wait_for_timeout(2000)

        close_buttons = [
            self.page.get_by_role("button", name="✕").first,
            self.page.get_by_role("button", name="X").first,
            self.page.locator("button").filter(has_text="✕").first,
            self.page.locator("[role='button']").filter(has_text="✕").first,
            self.page.locator("button._2KpZ6l._2doB4z").first,
        ]

        for close_btn in close_buttons:
            try:
                if close_btn.is_visible(timeout=1000):
                    close_btn.click(timeout=3000)
                    self.page.wait_for_timeout(500)
                    return
            except Exception:
                continue

        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(500)

    def close_popup(self):
        """Common popup close method for page objects."""
        self.close_login_popup()
