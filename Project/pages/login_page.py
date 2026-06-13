import re
from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def open_homepage(self):
        self.goto_url("https://www.flipkart.com")  # Navigate to the Flipkart homepage

    def click_login(self):
        # Click the 'Login' button in the header
        login_btn = self.page.get_by_role("link", name="Login").first
        if not login_btn.is_visible():
            login_btn = self.page.get_by_text("Login", exact=True).first

        login_btn.click()
        self.page.wait_for_timeout(2000)

    def enter_mobile(self, mobile):
       
        mobile_input = (
            self.page.locator("form")
            .filter(has_text=re.compile(r"Enter Email/Mobile number", re.I))
            .get_by_role("textbox")
            .first
        )
        mobile_input.wait_for(state="visible", timeout=5000)
        mobile_input.click()
        mobile_input.fill(str(mobile))

    def request_otp(self):
        otp_btn = self.page.get_by_role("button", name="Request OTP")
        otp_btn.wait_for(state="visible", timeout=5000)
        otp_btn.click(no_wait_after=True)

    def enter_otp(self, otp):
        otp_input = self.page.get_by_placeholder("Enter OTP")
        otp_input.wait_for(state="visible", timeout=5000)
        otp_input.fill(otp)

    @property
    def mobile_input(self):
        return self.page.locator("form").filter(has_text=re.compile(r"Enter Email/Mobile number", re.I)).get_by_role("textbox").first

    def click_verify(self):
        verify_btn = self.page.get_by_role("button", name="Verify")
        verify_btn.wait_for(state="visible", timeout=5000)
        verify_btn.click()
