from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import csv
import os

# Login page URL
LOGIN_URL = "https://practicetestautomation.com/practice-test-login/"

# Locators
USERNAME_ID = "username"
PASSWORD_ID = "password"
LOGIN_BUTTON_ID = "submit"
ERROR_MESSAGE_ID = "error"

# Test data
VALID_USERNAME = "student"
VALID_PASSWORD = "Password123"

INVALID_USERNAME = "wronguser"
INVALID_PASSWORD = "wrongpassword"

# Store test results
test_results = []

# Create screenshots folder
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


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


def take_screenshot(driver, test_case):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_case}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)

    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")

    return filepath


def add_result(test_case, status, remarks):
    test_results.append({
        "Test Case": test_case,
        "Status": status,
        "Remarks": remarks
    })


def test_valid_login(driver):
    print("Running TC01 - Valid Login Test...")

    try:
        login(driver, VALID_USERNAME, VALID_PASSWORD)
        time.sleep(2)

        if "logged-in-successfully" in driver.current_url:
            print("PASS: Valid login successful.")
            add_result(
                "TC01 - Valid Login",
                "PASS",
                "User successfully logged in."
            )
        else:
            screenshot = take_screenshot(driver, "TC01_Valid_Login")
            print("FAIL: Valid login failed.")
            add_result(
                "TC01 - Valid Login",
                "FAIL",
                f"User could not log in. Screenshot: {screenshot}"
            )

    except Exception as e:
        screenshot = take_screenshot(driver, "TC01_Valid_Login")
        add_result(
            "TC01 - Valid Login",
            "FAIL",
            f"{str(e)} | Screenshot: {screenshot}"
        )


def test_invalid_login(driver):
    print("Running TC02 - Invalid Login Test...")

    try:
        login(driver, INVALID_USERNAME, INVALID_PASSWORD)

        error = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.ID, ERROR_MESSAGE_ID)
            )
        )

        print(f"PASS: Error message displayed - {error.text}")
        add_result(
            "TC02 - Invalid Login",
            "PASS",
            error.text
        )

    except Exception as e:
        screenshot = take_screenshot(driver, "TC02_Invalid_Login")
        print("FAIL: Error message not displayed.")
        add_result(
            "TC02 - Invalid Login",
            "FAIL",
            f"{str(e)} | Screenshot: {screenshot}"
        )


def test_empty_fields(driver):
    print("Running TC03 - Empty Fields Test...")

    try:
        driver.get(LOGIN_URL)
        driver.find_element(By.ID, LOGIN_BUTTON_ID).click()
        time.sleep(2)

        if driver.current_url == LOGIN_URL:
            print("PASS: Validation for empty fields works.")
            add_result(
                "TC03 - Empty Fields",
                "PASS",
                "Validation for empty fields works."
            )
        else:
            screenshot = take_screenshot(driver, "TC03_Empty_Fields")
            print("FAIL: Empty fields validation failed.")
            add_result(
                "TC03 - Empty Fields",
                "FAIL",
                f"No validation for empty fields. Screenshot: {screenshot}"
            )

    except Exception as e:
        screenshot = take_screenshot(driver, "TC03_Empty_Fields")
        add_result(
            "TC03 - Empty Fields",
            "FAIL",
            f"{str(e)} | Screenshot: {screenshot}"
        )


def generate_report():
    print("\n" + "=" * 60)
    print("AUTOMATED TEST EXECUTION REPORT")
    print("=" * 60)

    passed = 0
    failed = 0

    for result in test_results:
        print(f"Test Case : {result['Test Case']}")
        print(f"Status    : {result['Status']}")
        print(f"Remarks   : {result['Remarks']}")
        print("-" * 60)

        if result["Status"] == "PASS":
            passed += 1
        else:
            failed += 1

    print(f"Total Tests : {len(test_results)}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")

    # Save report to CSV
    filename = f"Test_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Test Case", "Status", "Remarks"])

        for result in test_results:
            writer.writerow([
                result["Test Case"],
                result["Status"],
                result["Remarks"]
            ])

    print(f"\nReport saved as: {filename}")


# Main Execution
driver = setup_driver()

try:
    test_valid_login(driver)
    print("-" * 50)

    test_invalid_login(driver)
    print("-" * 50)

    test_empty_fields(driver)

finally:
    generate_report()
    driver.quit()
    print("\nBrowser closed.")