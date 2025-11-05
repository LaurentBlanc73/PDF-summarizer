import os
from flask import send_from_directory
from backend.main import api
from frontend.dash_app import dash_app

# single callable WSGI app
dash_app.init_app(api)
app = api


@api.route("/assets/<path:filename>")
def serve_assets(filename):
    assets_dir = os.path.join(os.path.dirname(__file__), "frontend", "assets")
    return send_from_directory(assets_dir, filename)
