import os
from dotenv import load_dotenv
from .call_backend import call_backend


def test_call_backend():
    # load and store env
    load_dotenv()
    original_env = os.environ.copy()

    # only for debugging GitHub Actions env issues
    assert os.getenv("BACKEND_BASE_URL") is not None

    # missing env var
    if "BACKEND_BASE_URL" in os.environ:
        del os.environ["BACKEND_BASE_URL"]
    response = call_backend("/summarize-text", {"key": "value"})
    assert response.status_code == 500
    assert response.json() == {"error": "Backend API is not configured on the server."}

    # wrong env var
    os.environ["BACKEND_BASE_URL"] = "http://invalid-url"
    response = call_backend("/summarize-text", {"key": "value"})
    assert response.status_code == 404
    assert "error" in response.json()
    assert "Backend API is not configured correctly on the server. Error: " in response.json()["error"]

    # restore env
    os.environ = original_env

    # test expected behavior
    response = call_backend("/summarize-text", {"text": "value"})
    assert response.status_code == 200
    assert "summary" in response.json()
    assert isinstance(response.json()["summary"], str)
