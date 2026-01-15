import os
import csv
import time

from dotenv import load_dotenv
from static import Locators as Sl
from util import (
    click_element, input_element,move_to_element,
    safe_navigate_to_url, check_element_exists
)


load_dotenv()
url = "https://atlas.heart.org/"
base_dir = os.path.dirname(os.path.abspath(__file__))
instructors_data_csv = os.path.join(base_dir, 'data', 'instructorList.csv')


def login(driver):
    def validate():
        if check_element_exists(driver, Sl.PROFILE_ICON, timeout=5):
            print("Login successful.")
        else:
            print("Login may have failed, dashboard not reached.")
    try:
        safe_navigate_to_url(driver, url)
        time.sleep(5)
        if check_element_exists(driver, Sl.PROFILE_ICON, timeout=5):
            print("Already logged in.")
            validate()
            return
        signin_button = check_element_exists(driver, Sl.SIGN_IN_BUTTON, timeout=5)
        if signin_button:
            click_element(driver, Sl.SIGN_IN_BUTTON)
            input_element(driver, Sl.USERNAME_INPUT, os.getenv("AHA_USERNAME"))
            input_element(driver, Sl.PASSWORD_INPUT, os.getenv("AHA_PASSWORD"))
            click_element(driver, Sl.SUBMIT_BUTTON)
        validate()
    except Exception as e:
        print(f"Login failed: {e}")


def capture_jwt_token(driver):
    try:
        token = driver.execute_script("return window.localStorage.getItem('userToken');")
        if token:
            return token
        else:
            print("JWT token not found in local storage.")
            return None
    except Exception as e:
        print(f"Failed to capture JWT token: {e}")
        return None


def navigate_to_class_listings(driver):
    try:
        move_to_element(driver, Sl.CLASSES_NAV)
        time.sleep(0.5)
        click_element(driver, Sl.TC_DROPDOWN)
        time.sleep(2)
        ORG_ALREADY_SELECTED = check_element_exists(driver, Sl.SELECTED_ORGANIZATION, timeout=3)
        if ORG_ALREADY_SELECTED:
            print("Organization already selected.\nSelected Organization `Shell CPR, LLC.`")
            return
        input_element(driver, Sl.ORGANIZATION_INPUT, "Shell CPR, LLC.")
        time.sleep(1)
        click_element(driver, Sl.ORGANIZATION_TO_SELECT)
        time.sleep(5)
    except Exception as e:
        print(f"Navigation to class listings failed: {e}")


def get_email_by_id(target_id):
    email_col = 6
    try:
        with open(instructors_data_csv, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > email_col:
                    current_id = row[5].strip()
                    if current_id == str(target_id):
                        return row[email_col]

        return None

    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: {e}"
