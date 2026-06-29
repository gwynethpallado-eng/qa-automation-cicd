from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Login page URL
LOGIN_URL = "https://practicetestautomation.com/practice-test-login/"

# Locators (change according to your website)
USERNAME_ID = "username"
PASSWORD_ID = "password"
LOGIN_BUTTON_ID = "submit"
ERROR_MESSAGE_ID = "error"

# Test data
VALID_USERNAME = "student"
VALID_PASSWORD = "Password123"

INVALID_USERNAME = "wronguser"
INVALID_PASSWORD = "wrongpassword"


def setup_driver():
    driver = webdriver.Edge()
    driver.maximize_window()
    return driver


def login(driver, username, password):
    driver.get(LOGIN_URL)

    driver.find_element(By.ID, USERNAME_ID).clear()
    driver.find_element(By.ID, USERNAME_ID).send_keys(username)

    driver.find_element(By.ID, PASSWORD_ID).clear()
    driver.find_element(By.ID, PASSWORD_ID).send_keys(password)

    driver.find_element(By.ID, LOGIN_BUTTON_ID).click()


def test_valid_login(driver):
    print("Running Valid Login Test...")

    login(driver, VALID_USERNAME, VALID_PASSWORD)

    time.sleep(2)

    if "dashboard" in driver.current_url:
        print("PASS: Valid login successful.")
    else:
        print("FAIL: Valid login failed.")


def test_invalid_login(driver):
    print("Running Invalid Login Test...")

    login(driver, INVALID_USERNAME, INVALID_PASSWORD)

    try:
        error = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.ID, ERROR_MESSAGE_ID)
            )
        )

        print(f"PASS: Error message displayed - {error.text}")

    except:
        print("FAIL: Error message not displayed.")


def test_empty_fields(driver):
    print("Running Empty Fields Test...")

    driver.get(LOGIN_URL)
    driver.find_element(By.ID, LOGIN_BUTTON_ID).click()

    time.sleep(2)

    if driver.current_url == LOGIN_URL:
        print("PASS: Validation for empty fields works.")
    else:
        print("FAIL: Empty fields validation failed.")


# Main execution
driver = setup_driver()

try:
    test_valid_login(driver)
    print("-" * 50)

    test_invalid_login(driver)
    print("-" * 50)

    test_empty_fields(driver)

finally:
    driver.quit()
    print("\nBrowser closed.")