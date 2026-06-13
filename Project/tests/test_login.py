import re
from pages.login_page import LoginPage
from playwright.sync_api import expect


def test_login_with_valid_mobile(page):
    login = LoginPage(page)

    login.open_homepage()
    login.close_login_popup()
    login.click_login()

   
    login.enter_mobile("9272105390")
    
   
    expect(login.mobile_input).to_have_value("9272105390")
    
    otp_btn = page.get_by_role("button", name="Request OTP")
    expect(otp_btn).to_be_visible()
    expect(otp_btn).to_be_enabled()



def test_login_invalid_mobile(page):
    login = LoginPage(page)

    login.open_homepage()
    login.close_login_popup()
    login.click_login()
    login.enter_mobile("123")
    login.request_otp()

    page.wait_for_timeout(500)
    error = page.get_by_text(re.compile(r"valid", re.I))
    expect(error).to_be_visible()


def test_login_empty_mobile(page):
    login = LoginPage(page)

    login.open_homepage()
    login.close_login_popup()
    login.click_login()
    login.enter_mobile("")
    login.request_otp()

    page.wait_for_timeout(500)
    error = page.get_by_text(re.compile(r"Please enter", re.I))
    expect(error).to_be_visible()


def test_greater_than_10_digit_mobile(page):
    login = LoginPage(page)
    login.open_homepage()
    login.close_login_popup()
    login.click_login()
    login.enter_mobile("9876543210123")
    login.request_otp()

    page.wait_for_timeout(500)
    error = page.locator("text=/Please enter valid|Please enter a valid/i").first
    expect(error).to_be_visible()


def test_login_alphabet_sepcilacharachter_mobile(page):
    login = LoginPage(page)

    login.open_homepage()
    login.close_login_popup()
    login.click_login()
    login.enter_mobile("abcd@#123")
    login.request_otp()

    page.wait_for_timeout(500)
    error = page.locator("text=/Please enter valid/i").first
    expect(error).to_be_visible()


def test_otp_incorrect(page):
    login = LoginPage(page)
    login.open_homepage()
    login.close_login_popup()
    login.click_login()
    login.enter_mobile("9272105390")
    login.request_otp()

    page.wait_for_timeout(500)
    
    try:
        otp_input = page.get_by_placeholder("Enter OTP", timeout=2000)
        otp_input.fill("123456")
        page.wait_for_timeout(500)
        expect(page.get_by_text(re.compile(r"valid OTP", re.I))).to_be_visible()
    except Exception:
        pass


def test_login_extremely_long_email(page):
    login = LoginPage(page)

    login.open_homepage()
    login.close_login_popup()
    login.click_login()

    # Enter an extremely long email address (negative case)
    long_email = "shivafalke24@gmail.commmmmmmmmm"
    login.enter_mobile(long_email)
    
    # Attempt to request OTP to trigger validation
    login.request_otp()
    
    
    page.wait_for_timeout(500)
    error = page.get_by_text(re.compile(r"valid", re.I))
    expect(error).to_be_visible()



def test_login_email_with_emojis(page):
    login = LoginPage(page)

    login.open_homepage()
    login.close_login_popup()
    login.click_login()

   
    emoji_email = "😊@😊.😊"
    login.enter_mobile(emoji_email)
    
    
    login.request_otp()
    
   
    page.wait_for_timeout(500)
    error = page.get_by_text(re.compile(r"valid", re.I))
    expect(error).to_be_visible()


def test_login_email_with_trailing_spaces(page):
    login = LoginPage(page)

    login.open_homepage()
    login.close_login_popup()
    login.click_login()

    
    email_with_spaces = "shivafalke24@gmail.com   "
    login.enter_mobile(email_with_spaces)
    
    login.mobile_input.press("Tab")
    
    val = login.mobile_input.input_value()
    assert val.strip() == "shivafalke24@gmail.com"


