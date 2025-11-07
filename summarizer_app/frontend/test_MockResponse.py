from .MockResponse import MockResponse


def test_MockResponse():
    # create a mock response object
    mock_response = MockResponse({"key": "value"}, 200, "mock reason")

    # test expected behavior
    assert mock_response.status_code == 200
    assert mock_response.json() == {"key": "value"}
    assert mock_response.reason == "mock reason"
