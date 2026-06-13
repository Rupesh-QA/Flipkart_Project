import re

from .base_page import BasePage
from utils.config import BASE_URL


class SignupPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.close_popup_btn = self.page.get_by_role("button", name="✕").first
        self.login_btn = self.page.get_by_text("Login", exact=True).first
        self.create_account_link = self.page.get_by_text("New to Flipkart?").first

        
        self.continue_btn = self.page.get_by_role("button", name="CONTINUE").first
        self.signup_btn = self.page.get_by_role("button", name="Signup").first
        self.resend_link = self.page.get_by_text("Resend?").first
        self.existing_user_link = self.page.get_by_text("Existing User?").first

    def open_homepage(self):
        self.page.goto(BASE_URL)

    def click_login(self):
        login_btn = self.page.get_by_role("link", name="Login").first
        if not login_btn.is_visible():
            login_btn = self.page.get_by_text("Login", exact=True).first
        login_btn.click()
        self.page.wait_for_timeout(2000)

    def click_create_account(self):
        self.create_account_link.wait_for(state="visible", timeout=5000)
        self.create_account_link.click()
        self.page.wait_for_timeout(2000)

    def enter_mobile(self, mobile):
       
        mobile_input = self.mobile_input
        mobile_input.wait_for(state="visible", timeout=5000)
        mobile_input.click()
        mobile_input.clear()
        mobile_input.fill(str(mobile))

    def click_continue(self):
        self.continue_btn.wait_for(state="visible", timeout=5000)
        self.continue_btn.click()

    def enter_otp(self, otp):
       
        otp_inputs = self.page.locator("input[type='tel']")
        for i, digit in enumerate(otp):
            otp_inputs.nth(i).fill(digit)

    def wait_for_otp_screen(self):
      
        self.page.locator("input[type='tel']").first.wait_for(
            state="visible", timeout=10000
        )

    @property
    def otp_inputs(self):
        """Used by test_signup_valid_mobile expectation"""
        return self.page.locator("input[type='tel']")

    @property
    def mobile_input(self):
        # Try multiple approaches to find the mobile input field
        # 1. First try: input with type='tel'
        tel_input = self.page.locator("input[type='tel']").first
        if tel_input:
            try:
                tel_input.wait_for(state="visible", timeout=2000)
                return tel_input
            except:
                pass
        
       
        text_input = self.page.locator("input[type='text'][maxlength='10']").first
        if text_input:
            try:
                text_input.wait_for(state="visible", timeout=2000)
                return text_input
            except:
                pass
        
       
        textbox = self.page.locator("form input[type='text']").first
       
        textbox.wait_for(state="visible", timeout=2000)
               
        
        
        return self.page.locator("form").filter(has_text="Enter Mobile numberBy").get_by_role("textbox").first

    def click_signup(self):
        self.signup_btn.wait_for(state="visible", timeout=5000)
        self.signup_btn.click()

    def click_resend(self):
        self.resend_link.wait_for(state="visible", timeout=5000)
        self.resend_link.click()

    def click_existing_user(self):
        self.existing_user_link.wait_for(state="visible", timeout=5000)
        self.existing_user_link.click()
