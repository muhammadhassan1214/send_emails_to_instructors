import os
import time
import random
from datetime import datetime
from dotenv import load_dotenv

from utils.apis.get_classes import get_classes
from utils.apis.get_class_info import get_class_details
from utils.apis.get_instructor_info import get_instructor_email
from utils.apis.get_coordinator_info import get_coordinator_email

from utils.mail_sender.email_sender import send_email
from utils.mail_sender.email_generator import generate_email

from utils.util import get_undetected_driver
from utils.automation import (
    capture_jwt_token, login,
    navigate_to_class_listings
)


load_dotenv()
SCHEDULE_INTERVAL_SECONDS = 12 * 60 * 60
done_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils", "data", "done_classes.txt")


def run_every_12_hours():
    print("Starting scheduled automation (runs every 12 hours)")
    run_count = 0

    while True:
        run_count += 1
        start = time.time()

        print(f"\n{'=' * 50}")
        print(f"SCHEDULED RUN #{run_count}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 50}")

        try:
            main()
        except Exception as e:
            print(f"Unhandled error in scheduled run #{run_count}: {e}")

        # --- Timing Logic ---
        elapsed = time.time() - start
        remaining = SCHEDULE_INTERVAL_SECONDS - elapsed

        if remaining > 0:
            next_run_timestamp = time.time() + remaining
            next_run_time = datetime.fromtimestamp(next_run_timestamp).strftime('%Y-%m-%d %H:%M:%S')

            print(f"Run #{run_count} completed in {elapsed:.1f}s")
            print(f"Next run scheduled for: {next_run_time}")

            # Converted log to show Hours instead of Minutes for clarity
            print(f"Waiting {remaining / 3600:.2f} hours...")

            time.sleep(remaining)
        else:
            print(f"Run #{run_count} took {elapsed:.1f}s (>= 12 hours). Starting next run immediately.")
            

def main():
    page_number = 0
    driver = get_undetected_driver(headless=True)
    try:
        login(driver)
        navigate_to_class_listings(driver)
        jwt_token = capture_jwt_token(driver)
        if driver:
            print("JWT token captured successfully.")
            driver.quit()
        while True:
            islast_page, classes = get_classes(page_number, jwt_token)
            if classes:
                print(f"Found {len(classes)} classes with enrolled students.")
                for cls in classes:
                    classId = str(cls.get("classId")).strip()
                    try:
                        with open(done_file_path, "r", encoding='utf-8') as f:
                            done_classes = [line.strip() for line in f.read().splitlines() if line.strip()]
                    except FileNotFoundError:
                        done_classes = []
                    if classId in done_classes:
                        print(f"Skipping already processed class {classId}")
                        continue
                    instructor_id = cls.get("instructorId")
                    instructor_name = cls.get("instructorName")
                    instructor_email, org_type, org_code = get_instructor_email(instructor_id, jwt_token)
                    class_details, students = get_class_details(classId, jwt_token)
                    coordinator_email = get_coordinator_email(org_type, org_code, jwt_token)
                    email_html = generate_email(instructor_name, students, class_details)
                    if class_details and students and instructor_email:
                        print(f"Sending email to {instructor_email} for class {classId}")
                        send_email(instructor_email, instructor_name, email_html)
                        send_email(os.getenv('NATHAN_EMAIL'), instructor_name, email_html)
                        if coordinator_email:
                            send_email(coordinator_email, instructor_name, email_html)
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
    run_every_12_hours()
