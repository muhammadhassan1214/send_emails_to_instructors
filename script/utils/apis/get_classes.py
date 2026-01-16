import json
import requests
from datetime import datetime, date, time
from ..static import ApiEndpoints


def extract_non_empty_classes(response: dict) -> tuple[bool, list[dict]]:
    results = []

    data = response.get("data", {})
    items = data.get("items", [])
    pagination = data.get("pagination", {})

    is_last = pagination.get("isLast", False)

    for item in items:
        occupied_seats = item.get("occupiedSeats", 0)

        # Skip if no occupied seats
        if occupied_seats == 0:
            continue

        instructor = item.get("primaryInstructor", {})

        results.append({
            "classId": item.get("classId"),
            "instructorId": instructor.get("instructorId", ""),
            "instructorName": instructor.get("instructorName", "")
        })

    return is_last, results


def get_today_and_year_end():
    # Local timezone-aware "now"
    now = datetime.now().astimezone()

    # Today's date (start of day)
    today_date = now.date()
    today_start = datetime.combine(today_date, time.min).astimezone()

    # End of ongoing year (start of 31 Dec)
    year_end_date = date(today_date.year, 12, 31)
    year_end_start = datetime.combine(year_end_date, time.min).astimezone()

    return {
        "today_epoch_ms": int(today_start.timestamp() * 1000),
        "today_date": today_date.strftime("%Y-%m-%d"),
        "year_end_epoch_ms": int(year_end_start.timestamp() * 1000),
        "year_end_date": year_end_date.strftime("%Y-%m-%d"),
    }


def get_classes(page_number: int, jwt_token: str):
    date_info = get_today_and_year_end()
    url = ApiEndpoints.GET_CLASSES(page_number)
    headers = ApiEndpoints.get_headers(jwt_token)

    payload = json.dumps({"classFilters":
      {"isFirstTsSelected": True,
       "courseId": None,
       "disciplineCodes": None,
       "seatAvailability": None,
       "langCode": None,
       "location": None,
       "classStatus": None,
       "isPrivate": None,
       "applyFilter": None,
       "applyTsFilter": None,
       "page": page_number,
       "pageNumber": page_number,
       "parentId": 18260,
       "size": 100,
       "instructorIds": [],
       "classStartDate": date_info.get("today_epoch_ms"),
       "classEndDate": date_info.get("year_end_epoch_ms"),
       "fromDate": date_info.get("today_date"),
       "toDate": date_info.get("year_end_date"),
       "selectedSort": "startDateTime",
       "sortOrder": "desc"
}})

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return extract_non_empty_classes(response.json())
    else:
        print(f"Failed to get classes on page {page_number}: {response.status_code}")
        return None, []
