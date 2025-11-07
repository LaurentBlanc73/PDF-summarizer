from dash import Dash, html, dcc, Input, Output, State, callback, no_update
from .call_backend import call_backend

dash_app = Dash(__name__, suppress_callback_exceptions=True)
server = dash_app.server


############################## layout ##############################
dash_app.layout = html.Div(
    [
        # layout
        html.H1("Summarize PDFs"),
        dcc.Upload(
            id="upload-file",
            children=html.Div(
                [
                    html.Div("Drag'n'Drop a PDF file", id="upload-box-text", className="upload-text-box"),
                    dcc.Loading(
                        id="spinner-upload",
                        type="circle",
                        color="grey",
                        children=html.Div(
                            id="upload-status",
                            style={"marginTop": "20px"},
                            children=html.Button("Choose File", id="upload-btn", className="upload-btn"),
                        ),
                    ),
                ],
                className="upload-box-content",
            ),
            accept="application/pdf",
            multiple=False,
            className="upload-box",
            className_active="upload-box-drag",
        ),
        html.H2("Summary", id="summary-header", className="h2"),
        html.Div(
            [
                dcc.Loading(
                    id="spinner-summary",
                    type="circle",
                    color="grey",
                    children=html.Div(
                        [
                            dcc.Textarea(
                                id="summary-text",
                                disabled=True,
                                draggable=False,
                                className="summary-text",
                            ),
                            dcc.Clipboard(
                                target_id="summary-text",
                                title="copy",
                                className="copy-btn",
                            ),
                        ],
                        className="summary-box-content",
                    ),
                ),
            ],
            id="summary-box",
            className="summary-box-passive",
        ),
        # variables
        dcc.Store(id="upload-enabled", data=True),
        dcc.Store(id="text", data=None),
    ],
    className="app-container",
)


############################# callbacks #############################
@callback(
    Output("upload-box-text", "children"),
    Output("upload-enabled", "data", allow_duplicate=True),
    Input("upload-file", "filename"),
    prevent_initial_call=True,
)
def update_upload_text(filename):
    """
    Generates a Dash HTML component displaying the uploaded PDF filename and icon.
    Args:
        filename (str): The name of the uploaded PDF file.
    Returns:
        tuple: A tuple containing the HTML Div component and a boolean value (False).
    """

    return (
        html.Div(
            [
                html.Div(className="stretch-box"),
                html.Img(src="/assets/pdf-icon.svg", className="pdf-icon", alt="PDF icon"),
                html.Div(filename, className="filename-text"),
            ],
            className="filename-box",
        ),
        False,
    )


@callback(
    Output("upload-file", "className"),
    Input("upload-enabled", "data"),
    prevent_initial_call=True,
)
def disable_enable_upload(upload_enabled):
    """
    Returns the appropriate CSS class for the upload box based on its enabled state.
    Args:
        upload_enabled (bool): Flag indicating whether the upload box should be enabled.
    Returns:
        str: CSS class name(s) for the upload box.
    """

    if upload_enabled:
        return "upload-box"
    else:
        return "upload-box upload-box-drop"


@callback(
    Output("upload-status", "children"),
    Output("text", "data"),
    Input("upload-enabled", "data"),
    State("upload-file", "contents"),
    prevent_initial_call=True,
)
def upload_file(upload_enabled, contents):
    """
    Handles file upload logic.
    Args:
        upload_enabled (bool): Flag indicating whether uploading is currently enabled.
        contents (str): The contents of the file to be uploaded.
    Returns:
        tuple: (html.Div, str) where the first element is a status message and the second is either the
            extracted text or an error message.
    """

    if upload_enabled:
        return no_update
    if not upload_enabled:
        # call backend
        response = call_backend(endpoint="/extract-text", json={"content": contents})

        if response.status_code == 200:  # success
            return (
                html.Div(
                    id="finished-upload",
                    children=[html.Span("✅"), html.Div(id="upload-btn-container", className="upload-btn-container")],
                ),
                response.json()["text"],
            )
        else:
            return (
                html.Div(
                    id="finished-upload",
                    children=[
                        html.Span("❌ Upload failed "),
                        html.Div(id="upload-btn-container", className="upload-btn-container"),
                    ],
                ),
                f"Reason for failed upload: {response.status_code} {response.json()}",
            )


@callback(
    Output("summary-text", "value"),
    Output("summary-box", "className"),
    Output("summary-header", "className"),
    Output("upload-enabled", "data", allow_duplicate=True),
    Input("upload-status", "children"),
    State("text", "data"),
    prevent_initial_call=True,
    suppress_callback_exceptions=True,
)
def display_summary(upload_status, text):
    """
    Generates and returns a summary for the provided text based on the upload status.
    If the upload status indicates a failed PDF upload, returns the failure reason.
    Otherwise, sends the text to a local summarization API and returns the summary or an error message.
    Args:
        upload_status: The status of the file upload, can be a Dash HTML Button or other status indicator.
        text (str): The text to be summarized or an error message from a failed upload.
    Returns:
        tuple: A tuple containing the summary text, CSS classes for styling, header classes, and a boolean flag.
    """

    if isinstance(upload_status, html.Button):
        return no_update

    if text.startswith("Reason for failed upload: "):  # pdf upload failed, nothing to summarize
        summary_text = text
    else:
        # call backend
        response = call_backend(endpoint="/summarize-text", json={"text": text})

        if response.status_code == 200:
            summary_text = response.json()["summary"]
        else:
            summary_text = (f"Reason for failed summary: {response.status_code}: {response.json()}",)

    return (
        summary_text,
        "summary-box-passive summary-box-active",
        "h2 h2-active",
        True,
    )


@callback(
    Output("upload-btn-container", "children"),
    Input("upload-enabled", "data"),
    prevent_initial_call=True,
)
def button_repeated_upload(upload_enabled):
    """
    Returns a file upload button component if uploading is enabled.
    Args:
        upload_enabled (bool): Flag indicating whether the upload button should be displayed.
    Returns:
        html.Button or no_update: The upload button component if enabled, otherwise a Dash no_update object.
    """

    if upload_enabled:
        return html.Button("Choose File", id="upload-btn", className="upload-btn")
    return no_update
