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


def get_class_details(class_id: str, jwt_token: str) -> dict:
    url = ApiEndpoints.GET_CLASS_DETAILS(class_id)
    headers = ApiEndpoints.get_headers(jwt_token)
    response = requests.get(url, headers=headers)
    print(F'Request made for fetching class details for class-ID {class_id}')
    if response.status_code == 200:
        return extract_class_details(response.json())
    else:
        print(f"Failed to get class details for class {class_id}: {response.status_code}")
        return {}
