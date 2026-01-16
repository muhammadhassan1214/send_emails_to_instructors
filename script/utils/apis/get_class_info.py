import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from ..static import ApiEndpoints


def extract_class_details(response: dict) -> dict:
    class_data = response.get("data", {}).get("class", {})

    # -------- Address --------
    address_details = (
        class_data
        .get("locationDetails", {})
        .get("addressDetails", {})
    )

    street1 = address_details.get("streetLine1", "")
    street2 = address_details.get("streetLine2", "")
    city = address_details.get("city", "")
    state = address_details.get("state", "")
    country = address_details.get("country", "")

    street = f"{street1} {street2}".strip() if street2 else street1

    location = ", ".join(filter(None, [street, city, state, country]))

    # -------- Class Start Date --------
    class_start_epoch = (
        class_data
        .get("scheduleInfoDetails", {})
        .get("classStartDate")
    )

    class_start_date = ""
    if class_start_epoch:
        dt = datetime.fromtimestamp(class_start_epoch / 1000, tz=ZoneInfo("America/New_York"))
        class_start_date = dt.strftime("%m-%d-%Y | %I:%M %p").lower()

    return {
        "date": class_start_date,
        "location": location
    }

def extract_student_contact_info(response: dict) -> list:
    results = []
    students = (
        response
        .get("data", {})
        .get("students", {})
        .get("items", [])
    )
    for student in students:
        results.append({
            "name": f'{student.get("firstName", "")} {student.get("lastName", "")}',
            "email": student.get("emailId", ""),
            "phone": student.get("phoneNumber", "")
        })

    return results


# validate responses
def responses_are_valid(class_response, students_response) -> bool:
    if class_response.status_code != 200:
        print(f"Failed to get class details: {class_response.status_code}")
        return False
    if students_response.status_code != 200:
        print(f"Failed to get students details: {students_response.status_code}")
        return False
    return True


# validate output data from responses
def extracted_data_is_valid(class_info: dict, student_info: list) -> bool:
    if class_info['date'] == "" or class_info['location'] == "":
        print("Class details extraction returned incomplete data.")
        return False
    for student in student_info:
        if student['name'] == "" or student['email'] == "":
            print(f"Student contact info extraction returned incomplete data.")
            return False
    return True


def get_class_details(class_id: str, jwt_token: str):
    class_url = ApiEndpoints.GET_CLASS_DETAILS(class_id)
    students_url = ApiEndpoints.GET_CLASS_STUDENTS(class_id)
    headers = ApiEndpoints.get_headers(jwt_token)

    class_response = requests.get(class_url, headers=headers)
    print(f'Request made for fetching class details for class-ID {class_id}')
    students_response = requests.get(students_url, headers=headers)
    print(f'Request made for fetching students details for class-ID {class_id}')

    if responses_are_valid(class_response, students_response):
        class_info = extract_class_details(class_response.json())
        student_info = extract_student_contact_info(students_response.json())

        if extracted_data_is_valid(class_info, student_info):
            return class_info, student_info
        else:
            return {}, []
    else:
        print(f"Failed to get class details for class {class_id}: {students_response.status_code}")
        return {}, []
