import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pytest
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager



# Compatibility testing for IMDb.com, contains the following tests:
# 1. Screen resolution compatibility:
# Validating size and visibility for: logo, menu, headline on default (13 inch laptop).
# Repeating tests after changing the viewport (S, M, L phones, average tablet).
# 2. Language compatibility:
# Verify that the website supports different languages correctly:
# Headline text, Menu text, Searchbar placeholder text testing in English, French, and German.
# 3. Browser compatibility:
# Repeat Screen Resolution test (originally done on Edge), on Firefox and Chrome.


# setup and teardown (fixture)
@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield
    driver.close()
    driver.quit()
    print("test completed")

# 1. Screen resolution compatibility:
# Fetching and validating logo's size and visibility on default (13 inch laptop)
def test_compatibility(test_setup):
    def set_viewport_size(driver, width, height):
        window_size = driver.execute_script(
            "return [window.outerWidth - window.innerWidth + arguments[0],"
            " window.outerHeight - window.innerHeight + arguments[1]];",
            width, height)
        driver.set_window_size(*window_size)

    # Open IMDb.com
    driver.get("https://www.imdb.com")
    # Find the logo element
    logo = driver.find_element_by_id("home_img_holder")
    # Find Headline text ("Featured Today")
    headline = driver.find_element_by_xpath("//*[@id='__next']/main/div/div[3]/div[2]/section/div[1]/hgroup/h3")
    # Find Menu element
    menu = driver.find_element_by_id("imdbHeader-navDrawerOpen")
    # Start testing
    logo_size = logo.size
    logo_visibility = logo.is_displayed()
    headline_size = headline.value_of_css_property("font-size")
    headline_visibility = headline.is_displayed()
    menu_size = menu.size
    menu_visibility = menu.is_displayed()
    # Validating data
    assert logo_size == {'height': 32, 'width': 64}
    assert logo_visibility == True
    assert headline_size == "32px"
    assert headline_visibility == True
    assert menu_size == {'height': 32, 'width': 97}
    assert menu_visibility == True

# Test changes in small mobile resolution (320X1050)
    small_mobile_width = 320
    small_mobile_height = 1050
    # Change the viewport size to small phone
    set_viewport_size(driver, small_mobile_width, small_mobile_height)
    # Testing after viewport change
    logo_size_S = logo.size
    logo_visibility_S = logo.is_displayed()
    headline_size_S = headline.value_of_css_property("font-size")
    headline_visibility_S = headline.is_displayed()
    menu_size_S = menu.size
    menu_visibility_S = menu.is_displayed()
    # Validating data
    assert logo_size_S == {'height': 32, 'width': 64}
    assert logo_visibility_S == True
    assert headline_size_S == "24px"
    assert headline_visibility_S == True
    assert menu_size_S == {'height': 48, 'width': 56}
    assert menu_visibility_S == True

# Test changes in medium mobile resolution (375X1050)
    medium_mobile_width = 375
    medium_mobile_height = 1050
    # Change the viewport size to medium phone
    set_viewport_size(driver, medium_mobile_width, medium_mobile_height)
    # Testing after viewport change
    logo_size_M = logo.size
    logo_visibility_M = logo.is_displayed()
    headline_size_M = headline.value_of_css_property("font-size")
    headline_visibility_M = headline.is_displayed()
    menu_size_M = menu.size
    menu_visibility_M = menu.is_displayed()
    # Validating data
    assert logo_size_M == {'height': 32, 'width': 64}
    assert logo_visibility_M == True
    assert headline_size_M == "24px"
    assert headline_visibility_M == True
    assert menu_size_M == {'height': 48, 'width': 56}
    assert menu_visibility_M == True

# Test changes in large mobile resolution (425X1050)
    large_mobile_width = 425
    large_mobile_height = 1050
    # Change the viewport size to large phone
    set_viewport_size(driver, large_mobile_width, large_mobile_height)
    # Testing after viewport change
    logo_size_L = logo.size
    logo_visibility_L = logo.is_displayed()
    headline_size_L = headline.value_of_css_property("font-size")
    headline_visibility_L = headline.is_displayed()
    menu_size_L = menu.size
    menu_visibility_L = menu.is_displayed()
    # Validating data
    assert logo_size_L == {'height': 32, 'width': 64}
    assert logo_visibility_L == True
    assert headline_size_L == "24px"
    assert headline_visibility_L == True
    assert menu_size_L == {'height': 48, 'width': 56}
    assert menu_visibility_L == True


# Test changes in average tablet resolution (768X1050)
    tablet_width = 768
    tablet_height = 1050
    # Change the viewport size to tablet
    set_viewport_size(driver, tablet_width, tablet_height)
    # Testing after viewport change
    logo_size_TAB = logo.size
    logo_visibility_TAB = logo.is_displayed()
    headline_size_TAB = headline.value_of_css_property("font-size")
    headline_visibility_TAB = headline.is_displayed()
    menu_size_TAB = menu.size
    menu_visibility_TAB = menu.is_displayed()
    # Validating data
    assert logo_size_TAB == {'height': 32, 'width': 64}
    assert logo_visibility_TAB == True
    assert headline_size_TAB == "32px"
    assert headline_visibility_TAB == True
    assert menu_size_TAB == {'height': 48, 'width': 56}
    assert menu_visibility_TAB == True


# 2. Verify that the website supports different languages correctly:
# Headline text, Menu text, Searchbar placeholder text testing in English, French, and German.
def test_localization(test_setup):
    driver.get("https://imdb.com")
    # Our value for testing - a headline with the text "Up next"
    up_next = driver.find_element_by_xpath("//*[@id='__next']/main/div/div[3]/div[1]/div/div/div[2]/div[1]/div[1]/span")
    # Second element to test - Menu text
    menu_text = driver.find_element_by_xpath("//*[@id='imdbHeader-navDrawerOpen']/span")
    # Third element to test - Searchbar placeholder text
    placeholder_text = driver.find_element_by_xpath("//input[@id='suggestion-search']")
# English test
    assert up_next.text == "Up next"
    assert menu_text.text == "Menu"
    assert placeholder_text.get_attribute("placeholder") == "Search IMDb"

# French test - Change language to French (choose from drop down menu then validate)
    dropdown = driver.find_element(By.XPATH, "//*[@id='imdbHeader']/div[2]/div[6]/label/span")
    dropdown.click()
    # Wait for the dropdown options to be visible
    wait = WebDriverWait(driver, 10)
    option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='sc-iklJRA sc-amhWr bbxMvA inZQkk navbar__flyout--breakpoint-m navbar__flyout--isVisible'] li[id='language-option-fr-FR'] span:nth-child(2)")))
    # Click the second option in the dropdown
    option.click()
    time.sleep(2)
    # Validate translation into French
    French_up_next = driver.find_element_by_xpath("//span[@class='sc-d4cb23a2-13 jtOKPy']")
    French_menu_text = driver.find_element_by_xpath("//*[@id='imdbHeader-navDrawerOpen']/span")
    French_placeholder = driver.find_element_by_xpath("//input[@id='suggestion-search']")
    assert French_up_next.text == "Suivante"
    assert French_menu_text.text == "Menu"
    assert French_placeholder.get_attribute("placeholder") == "Rechercher dans IMDb"

# German test - Change language to German (choose from drop down menu then validate)
    dropdown2 = driver.find_element(By.XPATH, "//*[@id='imdbHeader']/div[2]/div[6]/label/span")
    dropdown2.click()
    # Wait for the dropdown options to be visible
    wait = WebDriverWait(driver, 10)
    option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='sc-iklJRA sc-amhWr bbxMvA inZQkk navbar__flyout--breakpoint-m navbar__flyout--isVisible'] li[id='language-option-de-DE'] span:nth-child(2)")))
    # Click the second option in the dropdown
    option.click()
    time.sleep(2)
    # Validate translation into German
    German_up_next = driver.find_element_by_xpath("//span[@class='sc-d4cb23a2-13 jtOKPy']")
    German_menu_text = driver.find_element_by_xpath("//*[@id='imdbHeader-navDrawerOpen']/span")
    German_placeholder = driver.find_element_by_xpath("//input[@id='suggestion-search']")
    assert German_up_next.text == "Als Nächstes"
    assert German_menu_text.text == "Menü"
    assert German_placeholder.get_attribute("placeholder") == "IMDb durchsuchen"

# Browser Compatibility test - Firefox
def test_firefox():
    driver_firefox = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    def set_viewport_size_firefox(driver_firefox, width, height):
        window_size = driver_firefox.execute_script(
            "return [window.outerWidth - window.innerWidth + arguments[0],"
            " window.outerHeight - window.innerHeight + arguments[1]];",
            width, height)
        driver_firefox.set_window_size(*window_size)

    # Open IMDb.com
    driver_firefox.get("https://www.imdb.com")
    # Find the logo element
    logo = driver_firefox.find_element_by_id("home_img_holder")
    # Find Headline text ("Featured Today")
    headline = driver_firefox.find_element_by_xpath("//*[@id='__next']/main/div/div[3]/div[2]/section/div[1]/hgroup/h3")
    # Find Menu element
    menu = driver_firefox.find_element_by_id("imdbHeader-navDrawerOpen")
    # Start testing
    logo_size = logo.size
    logo_visibility = logo.is_displayed()
    headline_size = headline.value_of_css_property("font-size")
    headline_visibility = headline.is_displayed()
    menu_size = menu.size
    menu_visibility = menu.is_displayed()
    # Validating data
    assert logo_size == {'height': 32, 'width': 64}
    assert logo_visibility == True
    assert headline_size == "32px"
    assert headline_visibility == True
    assert menu_size == {'height': 32, 'width': 96.63333129882812}
    assert menu_visibility == True

    # Test changes in small mobile resolution (320X1050)
    small_mobile_width = 320
    small_mobile_height = 1050
    # Change the viewport size to small phone
    set_viewport_size_firefox(driver_firefox, small_mobile_width, small_mobile_height)
    # Testing after viewport change
    logo_size_S = logo.size
    logo_visibility_S = logo.is_displayed()
    headline_size_S = headline.value_of_css_property("font-size")
    headline_visibility_S = headline.is_displayed()
    menu_size_S = menu.size
    menu_visibility_S = menu.is_displayed()
    # Validating data
    assert logo_size_S == {'height': 32, 'width': 64}
    assert logo_visibility_S == True
    assert headline_size_S == "24px"
    assert headline_visibility_S == True
    assert menu_size_S == {'height': 48, 'width': 56}
    assert menu_visibility_S == True

    # Test changes in medium mobile resolution (375X1050)
    medium_mobile_width = 375
    medium_mobile_height = 1050
    # Change the viewport size to medium phone
    set_viewport_size_firefox(driver_firefox, medium_mobile_width, medium_mobile_height)
    # Testing after viewport change
    logo_size_M = logo.size
    logo_visibility_M = logo.is_displayed()
    headline_size_M = headline.value_of_css_property("font-size")
    headline_visibility_M = headline.is_displayed()
    menu_size_M = menu.size
    menu_visibility_M = menu.is_displayed()
    # Validating data
    assert logo_size_M == {'height': 32, 'width': 64}
    assert logo_visibility_M == True
    assert headline_size_M == "24px"
    assert headline_visibility_M == True
    assert menu_size_M == {'height': 48, 'width': 56}
    assert menu_visibility_M == True

    # Test changes in large mobile resolution (425X1050)
    large_mobile_width = 425
    large_mobile_height = 1050
    # Change the viewport size to large phone
    set_viewport_size_firefox(driver_firefox, large_mobile_width, large_mobile_height)
    # Testing after viewport change
    logo_size_L = logo.size
    logo_visibility_L = logo.is_displayed()
    headline_size_L = headline.value_of_css_property("font-size")
    headline_visibility_L = headline.is_displayed()
    menu_size_L = menu.size
    menu_visibility_L = menu.is_displayed()
    # Validating data
    assert logo_size_L == {'height': 32, 'width': 64}
    assert logo_visibility_L == True
    assert headline_size_L == "24px"
    assert headline_visibility_L == True
    assert menu_size_L == {'height': 48, 'width': 56}
    assert menu_visibility_L == True

    # Test changes in average tablet resolution (768X1050)
    tablet_width = 768
    tablet_height = 1050
    # Change the viewport size to tablet
    set_viewport_size_firefox(driver_firefox, tablet_width, tablet_height)
    # Testing after viewport change
    logo_size_TAB = logo.size
    logo_visibility_TAB = logo.is_displayed()
    headline_size_TAB = headline.value_of_css_property("font-size")
    headline_visibility_TAB = headline.is_displayed()
    menu_size_TAB = menu.size
    menu_visibility_TAB = menu.is_displayed()
    # Validating data
    assert logo_size_TAB == {'height': 32, 'width': 64}
    assert logo_visibility_TAB == True
    assert headline_size_TAB == "32px"
    assert headline_visibility_TAB == True
    assert menu_size_TAB == {'height': 48, 'width': 56}
    assert menu_visibility_TAB == True

    driver_firefox.quit()


# Browser Compatibility test - Chrome
def test_chrome():
    driver_chrome = webdriver.Chrome(executable_path=ChromeDriverManager().install())

    def set_viewport_size_chrome(driver_chrome, width, height):
        window_size = driver_chrome.execute_script(
            "return [window.outerWidth - window.innerWidth + arguments[0],"
            " window.outerHeight - window.innerHeight + arguments[1]];",
            width, height)
        driver_chrome.set_window_size(*window_size)

    # Open IMDb.com
    driver_chrome.get("https://www.imdb.com")
    # Find the logo element
    logo = driver_chrome.find_element_by_id("home_img_holder")
    # Find Headline text ("Featured Today")
    headline = driver_chrome.find_element_by_xpath("//*[@id='__next']/main/div/div[3]/div[2]/section/div[1]/hgroup/h3")
    # Find Menu element
    menu = driver_chrome.find_element_by_id("imdbHeader-navDrawerOpen")
    # Start testing
    logo_size = logo.size
    logo_visibility = logo.is_displayed()
    headline_size = headline.value_of_css_property("font-size")
    headline_visibility = headline.is_displayed()
    menu_size = menu.size
    menu_visibility = menu.is_displayed()
    # Validating data
    assert logo_size == {'height': 32, 'width': 64}
    assert logo_visibility == True
    assert headline_size == "32px"
    assert headline_visibility == True
    assert menu_size == {'height': 32, 'width': 96.63333129882812}
    assert menu_visibility == True

    # Test changes in small mobile resolution (320X1050)
    small_mobile_width = 320
    small_mobile_height = 1050
    # Change the viewport size to small phone
    set_viewport_size_chrome(driver_chrome, small_mobile_width, small_mobile_height)
    # Testing after viewport change
    logo_size_S = logo.size
    logo_visibility_S = logo.is_displayed()
    headline_size_S = headline.value_of_css_property("font-size")
    headline_visibility_S = headline.is_displayed()
    menu_size_S = menu.size
    menu_visibility_S = menu.is_displayed()
    # Validating data
    assert logo_size_S == {'height': 32, 'width': 64}
    assert logo_visibility_S == True
    assert headline_size_S == "24px"
    assert headline_visibility_S == True
    assert menu_size_S == {'height': 48, 'width': 56}
    assert menu_visibility_S == True

    # Test changes in medium mobile resolution (375X1050)
    medium_mobile_width = 375
    medium_mobile_height = 1050
    # Change the viewport size to medium phone
    set_viewport_size_chrome(driver_chrome, medium_mobile_width, medium_mobile_height)
    # Testing after viewport change
    logo_size_M = logo.size
    logo_visibility_M = logo.is_displayed()
    headline_size_M = headline.value_of_css_property("font-size")
    headline_visibility_M = headline.is_displayed()
    menu_size_M = menu.size
    menu_visibility_M = menu.is_displayed()
    # Validating data
    assert logo_size_M == {'height': 32, 'width': 64}
    assert logo_visibility_M == True
    assert headline_size_M == "24px"
    assert headline_visibility_M == True
    assert menu_size_M == {'height': 48, 'width': 56}
    assert menu_visibility_M == True

    # Test changes in large mobile resolution (425X1050)
    large_mobile_width = 425
    large_mobile_height = 1050
    # Change the viewport size to large phone
    set_viewport_size_chrome(driver_chrome, large_mobile_width, large_mobile_height)
    # Testing after viewport change
    logo_size_L = logo.size
    logo_visibility_L = logo.is_displayed()
    headline_size_L = headline.value_of_css_property("font-size")
    headline_visibility_L = headline.is_displayed()
    menu_size_L = menu.size
    menu_visibility_L = menu.is_displayed()
    # Validating data
    assert logo_size_L == {'height': 32, 'width': 64}
    assert logo_visibility_L == True
    assert headline_size_L == "24px"
    assert headline_visibility_L == True
    assert menu_size_L == {'height': 48, 'width': 56}
    assert menu_visibility_L == True

    # Test changes in average tablet resolution (768X1050)
    tablet_width = 768
    tablet_height = 1050
    # Change the viewport size to tablet
    set_viewport_size_chrome(driver_chrome, tablet_width, tablet_height)
    # Testing after viewport change
    logo_size_TAB = logo.size
    logo_visibility_TAB = logo.is_displayed()
    headline_size_TAB = headline.value_of_css_property("font-size")
    headline_visibility_TAB = headline.is_displayed()
    menu_size_TAB = menu.size
    menu_visibility_TAB = menu.is_displayed()
    # Validating data
    assert logo_size_TAB == {'height': 32, 'width': 64}
    assert logo_visibility_TAB == True
    assert headline_size_TAB == "32px"
    assert headline_visibility_TAB == True
    assert menu_size_TAB == {'height': 48, 'width': 56}
    assert menu_visibility_TAB == True

    driver_chrome.quit()
