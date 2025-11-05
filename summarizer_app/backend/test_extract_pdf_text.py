import pytest
import fitz
from .extract_pdf_text import extract_pdf_text, _clean_pages


def test_extract_pdf_text():
    # test for empty input
    assert "" == extract_pdf_text(content="")

    # test error paths
    with pytest.raises(ValueError, match="Input corrupted, missing ','"):
        extract_pdf_text("plain text")
    with pytest.raises(ValueError, match=r"Input has wrong type. Should be str, was .*"):
        extract_pdf_text(2)
    with pytest.raises(ValueError, match=r"Invalid base64-encoded string:.*"):
        extract_pdf_text(",JVBERi0xLjMgC")
    with pytest.raises(fitz.FileDataError, match="Cannot open empty stream"):
        extract_pdf_text("data,")
    with pytest.raises(fitz.FileDataError, match="Failed to open stream"):
        extract_pdf_text("data, asdf")
    with pytest.raises(ValueError, match="Incorrect padding"):
        extract_pdf_text("data,dd")


@pytest.mark.parametrize(
    "input, output_expected",
    [
        (["H"], [""]),  # 2 or less characters (usually not content)
        (["hh"], [""]),  # 2 or less characters (usually not content)
        (["44A"], [""]),  # more numbers than characters (usually not content)
        (["to."], ["to."]),  # possible ending of sentence (w/ minimal amount of letters)
        (
            ["header\ncontent1\nfooter", "header\ncontent2\nfooter"],
            ["content1", "content2"],
        ),  # header and footer removed
        (
            ["header\ncontent1 and footer in line", "header\ncontent2\nfooter"],
            ["content1 and footer in line", "content2\nfooter"],
        ),  # header removed but footer in line kept (not detected on 2. page since not present on 1. page)
        (
            ["content1", "header\ncontent2", "header\ncontent3"],
            ["content1", "content2", "content3"],
        ),  # header removed (present on most pages)
    ],
)
def test__clean_pages(input, output_expected):
    assert output_expected == _clean_pages(input)
