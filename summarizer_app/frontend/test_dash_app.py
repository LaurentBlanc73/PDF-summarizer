from dash import html, no_update
from .dash_app import upload_file, display_summary


def test_upload_file():
    # upload enabled (therefore no text to extract)
    return_value = upload_file(upload_enabled=True, contents="")
    assert return_value == no_update

    # upload not enabled (therefore text should be extracted)
    _, error_message = upload_file(upload_enabled=False, contents="Test content")
    assert "Reason for failed upload: " in error_message


def test_display_summary():
    # upload_status is button (therefore nothing to summarize)
    return_value = display_summary(upload_status=html.Button(), text="")
    assert return_value == no_update

    # text with error description of failed pdf upload
    text = "Reason for failed upload: some error"
    summary_text, _, _, _ = display_summary(upload_status="some status", text=text)
    assert summary_text == text

    # expected behavior
    text = "Test text"
    summary_text, _, _, _ = display_summary(upload_status="some status", text=text)
    assert isinstance(summary_text, str)
