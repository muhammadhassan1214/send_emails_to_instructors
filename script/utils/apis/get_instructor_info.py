import requests
from ..static import ApiEndpoints


def extract_email_from_response(response_data):
    try:
        items = response_data.get("data", {}).get("items", [])
        for item in items:
            email = item.get("email")
            org_type = item.get("orgType")
            org_code = item.get("orgCode")
            if email:
                return email, org_type, org_code
        return None

    except AttributeError:
        return None


def get_instructor_email(instructor_id: str, jwt_token: str):
    url = ApiEndpoints.GET_INSTRUCTOR_INFO(instructor_id)
    headers = ApiEndpoints.get_headers(jwt_token)

    response = requests.get(url, headers=headers)
    print(f'Request made for fetching instructor email for instructor-ID {instructor_id}')
    if response.status_code != 200:
        print(f"Failed to get instructor email: {response.status_code}")
        return None
    return extract_email_from_response(response.json())
