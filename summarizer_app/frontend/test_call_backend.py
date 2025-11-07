import os
from dotenv import load_dotenv
from .call_backend import call_backend


def test_call_backend_missing_env_var(monkeypatch):
    # load env
    load_dotenv()

    # missing env var
    if "BACKEND_BASE_URL" in os.environ:
        monkeypatch.delenv("BACKEND_BASE_URL")
    response = call_backend("/summarize-text", {"key": "value"})
    assert response.status_code == 500
    assert response.json() == {"error": "Backend API is not configured on the server."}


def test_call_backend_wrong_env_var(monkeypatch):
    # load env
    load_dotenv()

    # wrong env var
    monkeypatch.setenv("BACKEND_BASE_URL", "http://invalid-url")
    response = call_backend("/summarize-text", {"key": "value"})
    assert response.status_code == 404
    assert "error" in response.json()
    assert "Backend API is not configured correctly on the server. Error: " in response.json()["error"]


def test_call_backend_success():
    # load env
    load_dotenv()

    # test expected behavior
    response = call_backend("/summarize-text", {"text": "value"})
    assert response.status_code == 200
    assert "summary" in response.json()
    assert isinstance(response.json()["summary"], str)
