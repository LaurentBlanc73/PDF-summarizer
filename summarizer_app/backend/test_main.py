import pytest
from .main import api


@pytest.mark.parametrize(
    "input, status_code, error_msg",
    [
        (4, 415, "input was not a json, was <class 'int'>"),
        ({"wrongKey": None}, 400, "missing field 'content'"),
        ({"content": None}, 400, "missing field 'content'"),
        ({"content": 1}, 415, "content must be of type str, was <class 'int'>"),
        ({"content": "", "second_key": None}, 400, "unexpected additional JSON fields"),
        ({"content": ""}, 415, "content must be a 'data:application/pdf;' URI"),
        ({"content": "wrong formatted"}, 415, "content must be a 'data:application/pdf;' URI"),
        ({"content": "data:application/pdf;wrongEncodingScheme"}, 415, "content must be base64-encoded"),
        ({"content": "data:application/pdf;base64,"}, 422, "Invalid or empty PDF"),
        ({"content": "data:application/pdf;base64,dd"}, 422, "Incorrect padding"),
    ],
)
def test_extract_text(input, status_code, error_msg):
    client = api.test_client()
    response = client.post("/extract-text", json=input)

    assert response.status_code == status_code
    assert response.get_json() == {"error": error_msg}


@pytest.mark.parametrize(
    "input, status_code, msg_type, msg",
    [
        (4, 415, "error", "input was not a json, was <class 'int'>"),
        ({"wrongKey": None}, 400, "error", "missing field 'text'"),
        ({"text": None}, 400, "error", "missing field 'text'"),
        ({"text": 1}, 415, "error", "text must be of type str, was <class 'int'>"),
        ({"text": "", "second_key": None}, 400, "error", "unexpected additional JSON fields"),
        ({"text": ""}, 200, "summary", ""),
        ({"text": "This is a test article to summarize."}, 200, "summary", "test"),
    ],
)
def test_summarize_text(input, status_code, msg_type, msg):
    client = api.test_client()
    response = client.post("/summarize-text", json=input)
    data = response.get_json()

    assert response.status_code == status_code
    assert msg_type in data.keys()
    assert msg in data[msg_type]
