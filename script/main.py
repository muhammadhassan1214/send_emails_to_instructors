import os
import time
import random
from dotenv import load_dotenv

from utils.apis.get_classes import get_classes
from utils.apis.get_class_info import get_class_details
from utils.apis.get_student_info import get_students_in_class

from utils.mail_sender.email_sender import send_email
from utils.mail_sender.email_generator import generate_email

from utils.util import get_undetected_driver
from utils.scheduler import schedule_morning_and_night
from utils.automation import (
    capture_jwt_token, get_email_by_id,
    login, navigate_to_class_listings
)


load_dotenv()
done_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils", "data", "done_classes.txt")

def main():
    page_number = 0
    driver = get_undetected_driver()
    try:
        login(driver)
        navigate_to_class_listings(driver)
        jwt_token = capture_jwt_token(driver)
        while True:
            islast_page, classes = get_classes(page_number, jwt_token)
            if classes:
                print(f"Found {len(classes)} classes with enrolled students.")
                for cls in classes:
                    classId = cls.get("classId")
                    with open(done_file_path, "r") as f:
                        done_classes = f.read().splitlines()
                    if classId in done_classes:
                        print(f"Skipping already processed class {classId}")
                        continue
                    instructor_id = cls.get("instructorId")
                    instructor_name = cls.get("instructorName")
                    instructor_email = get_email_by_id(instructor_id)
                    class_details = get_class_details(classId, jwt_token)
                    students = get_students_in_class(classId, jwt_token)
                    email_html = generate_email(instructor_name, students, class_details)
                    if instructor_email:
                        print(f"Sending email to {instructor_email} for class {classId}")
                        send_email(instructor_email, instructor_name, email_html)
                        send_email(os.getenv('NATHAN_EMAIL'), instructor_name, email_html)
                    else:
                        print(f"No email found for instructor ID {instructor_id}")
                    with open(done_file_path, "a", encoding='utf-8') as f:
                        f.write(f"{classId}\n")
            else:
                print(f"No classes with enrolled students found on page {page_number + 1}.")

            page_number += 1
            time.sleep(random.randint(1, 3))
            if islast_page:
                print("All pages processed.")
                break

    except Exception as e:
        print(f"An error occurred in main: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    schedule_morning_and_night(main)
