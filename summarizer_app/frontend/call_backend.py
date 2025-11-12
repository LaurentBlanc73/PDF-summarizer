import os
import requests
from .MockResponse import MockResponse


def call_backend(endpoint: str, json: dict) -> requests.Response:
    """
    Sends a POST request to the backend API with the specified endpoint and JSON.
    Args:
        endpoint (str): The API endpoint to call.
        json (dict): The JSON to send in the POST request.
    Returns:
        requests.Response: The response object from the backend API or a mock response if backend is not configured or a request error occurs.
    """

    # get env variables
    BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL")
    BACKEND_API_KEY = os.getenv("BACKEND_API_KEY")
    if not BACKEND_BASE_URL or not BACKEND_API_KEY:
        response = MockResponse({"error": "Backend API is not configured on the server."}, 500)
        return response

    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"
    try:
        full_url = f"{BACKEND_BASE_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {BACKEND_API_KEY}"}
        response = requests.post(full_url, headers=headers, json=json, timeout=25)
        if response.status_code != 200:
            response = MockResponse(
                {"error": f"There was an error at the backend API. Error: {response.reason}"},
                response.status_code,
            )
        return response
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.Timeout):
            response = MockResponse(
                {"error": "There was a timeout while accessing the backend API. Try again in a couple minutes."}, 504
            )
            return response
        response = MockResponse({"error": f"There was an error accessing the backend API. Error: {e}"}, 500)
        return response
    except Exception as e:
        response = MockResponse({"error": f"An unexpected error occurred. Error: {e}"}, 500)
        return response
