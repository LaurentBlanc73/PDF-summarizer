import os
from dotenv import load_dotenv
from .call_backend import call_backend


def test_call_backend_missing_env_vars(monkeypatch):
    # load env
    load_dotenv()

    # missing env var
    if "BACKEND_BASE_URL" in os.environ:
        monkeypatch.delenv("BACKEND_BASE_URL")
    if "BACKEND_API_KEY" in os.environ:
        monkeypatch.delenv("BACKEND_API_KEY")
    response = call_backend("/summarize-text", {"key": "value"})
    assert response.status_code == 500
    assert response.json() == {"error": "Backend API is not configured on the server."}


def test_call_backend_wrong_env_backend_base_url(monkeypatch):
    # load env
    load_dotenv()

    # wrong backend base url in env
    monkeypatch.setenv("BACKEND_BASE_URL", "http://invalid-url")
    response = call_backend("/summarize-text", {"key": "value"})
    assert response.status_code == 500  # only True for clean test environment (not on local machine)
    assert response.json() == {
        "error": "There was an error accessing the backend API."
    }  # only True for clean test environment (not on local machine)


def test_call_backend_wrong_env_backend_api_key(monkeypatch):
    # load env
    load_dotenv()

    # wrong backend api key in env
    monkeypatch.setenv("BACKEND_API_KEY", "dummy_api_key")
    response = call_backend("/summarize-text", {"key": "value"})
    assert response.status_code == 401
    assert response.json() == {"error": "There was an error at the backend API. Error: UNAUTHORIZED"}


def test_call_backend_wrong_endpoint():
    # load env
    load_dotenv()

    # wrong endpoint
    response = call_backend("/wrong-endpoint", {"key": "value"})
    assert response.status_code == 404
    assert "error" in response.json()
    assert "There was an error at the backend API. Error: " in response.json()["error"]


def test_call_backend_success():
    # load env
    load_dotenv()

    # test expected behavior
    response = call_backend("/summarize-text", {"text": "value"})
    assert response.status_code == 200
    assert "summary" in response.json()
    assert isinstance(response.json()["summary"], str)
