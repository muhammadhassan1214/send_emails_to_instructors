import requests
from script.utils.static import ApiEndpoints


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


def get_students_in_class(class_id: str, jwt_token: str) -> list:
    url = ApiEndpoints.GET_CLASS_STUDENTS(class_id)
    headers = ApiEndpoints.get_headers(jwt_token)
    response = requests.get(url, headers=headers)
    print(response.json())
    print(f'Request made for fetching students details for class-ID {class_id}')
    if response.status_code == 200:
        return extract_student_contact_info(response.json())
    else:
        print(f"Failed to get students for class {class_id}: {response.status_code}")
        return []
