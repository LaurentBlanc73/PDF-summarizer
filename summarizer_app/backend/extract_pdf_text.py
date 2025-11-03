import base64
import pymupdf
import fitz
import numpy as np


def _get_headers_footers(pages: list) -> list:
    """
    # get repeated lines (must be present on most pages)
    """

    # smallest page contains at least header/footer and takes least computing
    smallest_page = pages[np.argmin([len(page) for page in pages[1:]]) + 1]  # headers often start at 2. page
    smallest_page_lines = [line for line in smallest_page.split("\n")]

    # check for repeating lines
    repeated_lines = []
    pages_total = len(pages)
    for line in smallest_page_lines:
        line_count = 0
        page_idx = 0

        # line must be present on at least half of the pages
        while (line_count < int(pages_total / 2) + 1) and page_idx <= pages_total - 1:
            page_lines = pages[page_idx].split("\n")
            if any(line == page_line for page_line in page_lines):
                line_count += 1
            page_idx += 1

        if line_count >= int(pages_total / 2) + 1:
            repeated_lines.append(line)

    return repeated_lines


def _clean_pages(pages: list) -> list:
    # get header and footer lines
    if len(pages) > 1:
        headers_footers = _get_headers_footers(pages)

    for i, page in enumerate(pages):
        page_lines = page.split("\n")

        # clean header and footer (by getting rid of lines that occur on every page)
        if len(pages) > 1:  # only works for multiple pages
            page_lines = [line for line in page_lines if line not in headers_footers]

        # clean lines w/ two or less characters (those are usually not content)
        page_lines = [line for line in page_lines if len(line.replace(" ", "")) > 2]
        # clean lines w/ more numbers than characters (those are usually not content)
        page_lines = [line for line in page_lines if sum(c.isalpha() for c in line) / len(line.replace(" ", "")) > 0.5]

        pages[i] = "\n".join(page_lines)

    return pages


def extract_pdf_text(content: str) -> str:
    # return empty string for empty input
    if content == "":
        return ""

    # validate input
    if not isinstance(content, str):
        raise ValueError(f"Input has wrong type. Should be str, was {type(content)}")
    if "," not in content:  # separates metadata from data
        raise ValueError("Input corrupted, missing ','")

    # extract text from pdf document
    base64_data = content.split(",")[1]
    pdf_bytes = base64.b64decode(base64_data)
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    pages = [page.get_text() for page in pdf_document]
    pdf_document.close()

    # clean pages
    pages = _clean_pages(pages)

    # create single string
    pdf_str = "\n".join(pages)

    return pdf_str
