class MockResponse:
    """A mock response object for handling internal configuration errors."""

    def __init__(self, json_data, status_code, reason=""):
        self._json_data = json_data
        self.status_code = status_code
        self.reason = reason

    def json(self):
        """Returns the JSON data."""
        return self._json_data
