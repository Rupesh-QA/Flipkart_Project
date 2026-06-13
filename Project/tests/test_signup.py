from pages.signup_page import SignupPage
from playwright.sync_api import expect


def setup_signup(page):
    signup = SignupPage(page)
    signup.open_homepage()
    signup.close_popup()
    signup.click_login()
    signup.click_create_account()
    return signup


def test_signup_valid_mobile(page):
    """Test signup with a valid dummy number"""
    signup = setup_signup(page)

    mobile_input = signup.mobile_input
    mobile_input.wait_for(state="visible", timeout=3000)

    # Capture value immediately after filling
    mobile_input.fill("9999999991")
    captured_value = mobile_input.input_value()


    assert captured_value == "9999999991"

   
    expect(signup.continue_btn).to_be_visible()
    expect(signup.continue_btn).to_be_enabled()



def test_signup_invalid_mobile(page):
    """Test signup with invalid short mobile"""
    signup = setup_signup(page)

    mobile_input = signup.mobile_input
    mobile_input.wait_for(state="visible", timeout=3000)
    mobile_input.fill("123")

    captured_value = mobile_input.input_value()
    assert captured_value == "123"
    signup.click_continue()

def test_signup_empty_mobile(page):
    """Test signup with empty mobile - should show validation error"""
    signup = setup_signup(page)

    mobile_input = signup.mobile_input
    mobile_input.wait_for(state="visible", timeout=3000)
    mobile_input.fill("")

    continue_btn = signup.continue_btn
    continue_btn.click()

    page.wait_for_timeout(500)
    expect(page.locator("text=/Please enter/i")).to_be_visible()


def test_signup_existing_user(page):
    """Test signup with already registered number"""
    signup = setup_signup(page)

    mobile_input = signup.mobile_input
    mobile_input.wait_for(state="visible", timeout=3000)
    mobile_input.fill("9272105390")

    continue_btn = signup.continue_btn
    continue_btn.click()

    page.wait_for_timeout(500)
    expect(page.locator("text=/already registered|existing/i").first).to_be_visible()


def test_signup_greater_than_10_digit_mobile(page):
    """Test signup input field accepts only up to 10 digits"""
    signup = setup_signup(page)

    mobile_input = signup.mobile_input
    mobile_input.wait_for(state="visible", timeout=3000)
    mobile_input.fill("12345678901234")

   
    assert len(mobile_input.input_value()) <= 10
    

def test_signup_mobile_with_alphabets(page):
    """Test signup - alphabets should be stripped"""
    signup = setup_signup(page)

    mobile_input = signup.mobile_input
    mobile_input.wait_for(state="visible", timeout=3000)
    mobile_input.fill("abcd123")

    # Flipkart strips alphabets, keeps only digits
    actual_value = mobile_input.input_value()
    assert actual_value == "123"


def test_signup_mobile_mixed_input(page):
    """Test signup - mixed alphanumeric should strip letters"""
    signup = setup_signup(page)

    mobile_input = signup.mobile_input
    mobile_input.wait_for(state="visible", timeout=3000)
    mobile_input.fill("9876abc123")

   
    actual_value = mobile_input.input_value()
    assert actual_value == "9876123"


def test_signup_mobile_with_emojis(page):
    """Test signup - mobile with emojis should strip emojis"""
    signup = setup_signup(page)

    mobile_input = signup.mobile_input
    mobile_input.wait_for(state="visible", timeout=3000)
    mobile_input.fill("9999999991😊")

    # Verify emojis are stripped
    actual_value = mobile_input.input_value()
    assert actual_value == "9999999991"


def test_signup_mobile_with_trailing_spaces(page):
    """Test signup - mobile with trailing spaces and tab shifting focus"""
    signup = setup_signup(page)

    mobile_input = signup.mobile_input
    mobile_input.wait_for(state="visible", timeout=3000)
    mobile_input.fill("9999999991   ")

   
    mobile_input.press("Tab")

   
    actual_value = mobile_input.input_value()
    assert actual_value.strip() == "9999999991"

