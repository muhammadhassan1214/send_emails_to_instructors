import requests
from ..static import ApiEndpoints


def get_coordinator_email_from_response(response_data):
    try:
        items = response_data.get("data", {}).get("items", [])

        # 2. Loop through items to find the email
        for item in items:
            # Access organisationProfile (handle if it is None)
            org_profile = item.get("organisationProfile")
            if not org_profile:
                continue

            # Access coordinator (handle if it is None)
            coordinator = org_profile.get("coordinator")
            if not coordinator:
                continue

            # Access email
            email = coordinator.get("email")
            if email:
                return email

        return None

    except AttributeError:
        return None


def get_coordinator_email(coordinator_id: str, coordinator_type: str, jwt_token: str):
    url = ApiEndpoints.GET_COORDINATOR_INFO(coordinator_id, coordinator_type)
    headers = ApiEndpoints.get_headers(jwt_token)

    response = requests.get(url, headers=headers)
    print(f'Request made for fetching coordinator info for coordinator-ID {coordinator_id}')
    if response.status_code != 200:
        print(f"Failed to get coordinator info: {response.status_code}")
        return None
    return get_coordinator_email_from_response(response.json())
