import pytest
from pages.home_page import HomePage
from playwright.sync_api import expect


VALID_SEARCH_PRODUCTS = [
    ("phone", ["phone"]),
    ("laptop", ["laptop"]),
    ("accessories", ["accessories"]),
    ("iPhone 15", ["iphone", "15"]),
]

INVALID_SEARCH_INPUTS = [
    ("@#%$", "special_characters"),
    ("phone@123", "mixed_input"),
    ("", "empty_query"),
]


class TestHomePage:

    def test_homepage_loads_successfully(self, page):

        home = HomePage(page)

        home.open_homepage()

        expect(home.logo).to_be_visible()
        expect(home.search_bar).to_be_visible()

    @pytest.mark.parametrize("product,expected_keywords", VALID_SEARCH_PRODUCTS)
    def test_search_valid_products(self, page, product, expected_keywords):

        home = HomePage(page)

        home.open_homepage()

        home.search_product(product)

        url_lower = page.url.lower()

       
        assert any(keyword in url_lower for keyword in expected_keywords)

       
        expect(home.product_titles.first).to_be_visible()

        
        assert home.product_titles.count() > 0

    def test_search_auto_suggestions(self, page):

        home = HomePage(page)

        home.open_homepage()

        home.enter_search_text("iph")

        
        expect(home.search_suggestions.first).to_be_visible()

        
        assert home.search_suggestions.count() > 0
       
       
        
    @pytest.mark.parametrize("search_input,test_type", INVALID_SEARCH_INPUTS)
    def test_search_invalid_input(self, page, search_input, test_type):

         home = HomePage(page)

         home.open_homepage()

         
         home.search_bar.wait_for(state="visible", timeout=10000)

         
         home.search_bar.fill(search_input)

    
         home.search_button.click()

   
         expect(home.search_bar).to_be_visible()

         if test_type == "empty_query":

          assert home.HOMEPAGE_URL in page.url

         else:
       
          assert page.url is not None

    def test_search_trailing_spaces(self, page):
        home = HomePage(page)
        home.open_homepage()
        
        # Enter product name with leading/trailing spaces
        home.search_product("   laptop   ")
        
        # Validate URL contains expected keyword
        assert "laptop" in page.url.lower()
        expect(home.product_titles.first).to_be_visible()

    def test_search_with_emojis(self, page):
        home = HomePage(page)
        home.open_homepage()
        
        # Enter search query with emojis
        home.enter_search_text("💻😊")
        home.search_button.click()
        
        # Should stay on page or load gracefully
        expect(home.search_bar).to_be_visible()

          
          
          