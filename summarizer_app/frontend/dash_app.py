from dash import Dash, html, dcc, Input, Output, State, callback, no_update, callback_context
import requests
import pickle  # TODO: delete

dash_app = Dash(__name__, suppress_callback_exceptions=True)

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


@callback(
    Output("upload-box-text", "children"),
    Output("upload-enabled", "data", allow_duplicate=True),
    Input("upload-file", "filename"),
    prevent_initial_call=True,
)
def update_upload_text(filename):
    return (
        html.Div(
            [
                html.Div(className="stretch-box"),
                html.Img(src="/assets/pdf-icon.svg", className="pdf-icon", alt="PDF icon"),  # change
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
    if upload_enabled:
        return "upload-box"
    else:
        return "upload-box upload-box-drop"


@callback(
    Output("upload-status", "children"),
    Output("text", "data"),
    Input("upload-enabled", "data"),
    State("upload-file", "contents"),
    # State("upload-file", "filename"),  # TODO: delete
    prevent_initial_call=True,
)
def upload_file(upload_enabled, contents):
    if upload_enabled:
        return no_update
        # return html.Button("Choose File", id="upload-btn", className="upload-btn")
    if not upload_enabled:

        # with open(f"{filename}.pkl", "wb") as f:  # TODO: delete
        #    pickle.dump(contents, f)

        # call backend
        url = "http://127.0.0.1:5000/extract-text"  # TODO: keep somewhere else? (maybe in a dedicated config file)
        response = requests.post(url, json={"content": contents})

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
    # if upload_status["props"]["children"][0]["props"]["children"] != "✅":
    #    return no_update
    if isinstance(upload_status, html.Button):  # works -> delete lines above
        return no_update

    if text.startswith("Reason for failed upload: "):  # pdf upload failed, nothing to summarize
        summary_text = text
    else:
        url = "http://127.0.0.1:5000/summarize-text"  # TODO: keep somewhere else? (maybe in a dedicated config file)
        response = requests.post(url, json={"text": text})

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
    if upload_enabled:
        return html.Button("Choose File", id="upload-btn", className="upload-btn")
    return no_update


if __name__ == "__main__" and False:  # TODO: delete and False
    dash_app.run(debug=True)


# not needed: first implementation of uploading display
"""
@callback(
    Output("upload-display", "children"),
    Output("upload-state", "data"),
    Output("spinner-activate", "data"),
    # Input("upload-file", "filename"),
    # Input("upload-file", "contents"),
    prevent_initial_call=True,
)
def upload_display(filename, contents):
    print("in upload display")
    # render upload display during upload
    return (
        html.Div(
            [
                html.Div(
                    [
                        html.Img(src="/assets/pdf-icon.svg", className="pdf-icon", alt="PDF icon"),
                        html.Span(filename, className="filename-text"),
                    ],
                    className="filename-box",
                ),
                dcc.Loading(
                    id="spinner-upload",
                    type="circle",
                    children=html.Div(id="upload-status", style={"marginTop": "20px"}),
                ),
            ],
            className="upload-box-content",
        ),
        "uploading",
        True,
    )
"""

# not needed: render depending on desktop or mobile
"""
@callback(
    Output("upload-file", "children"),
    # Output("upload-status", "children"),
    Input("upload-file", "filename"),
    Input("upload-file", "contents"),
    State("platform-info", "data"),
    prevent_initial_call=True,
)
def upload_file(filename, contents, platform):

    print(filename)
    # print(f"content: {contents}")

    # display file uploading
    if platform in ["Windows", "Darwin", "Linux"]:
        # desktop
        return html.Div(
            [
                html.Div(
                    [
                        html.Img(src="/assets/pdf-icon.svg", className="pdf-icon", alt="PDF icon"),
                        html.Span(filename, className="filename-text"),
                    ],
                    className="filename-box",
                ),
                dcc.Loading(id="spinner-upload", type="circle", children=html.Div(id="upload-status")),
            ],
            className="upload-box-content",
        )
    else:
        # mobile
        return html.Div(
            html.Div(
                [
                    html.Img(src="/assets/pdf-icon.svg", className="pdf-icon", alt="PDF icon"),
                    html.Span(filename, className="filename-text"),
                ],
                className="filename-box",
            ),
            className="upload-box-content",
        )
"""
