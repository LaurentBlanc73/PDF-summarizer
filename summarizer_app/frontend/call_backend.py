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
    if not BACKEND_BASE_URL:
        response = MockResponse({"error": "Backend API is not configured on the server."}, 500)
        return response

    full_url = f"{BACKEND_BASE_URL}{endpoint}"
    try:
        response = requests.post(full_url, json=json)
        if response.status_code != 200:
            response = MockResponse(
                {"error": f"Backend API is not configured correctly on the server. Error: {response.reason}"},
                response.status_code,
            )
        return response
    except requests.exceptions.RequestException as e:
        response = MockResponse({"error": "There was an error accessing the backend API."}, 500)
        return response
