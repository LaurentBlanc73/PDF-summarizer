from threading import Thread
from backend.main import api
from frontend.dash_app import dash_app


def run_api():
    api.run(host="0.0.0.0", port=5000)


def run_dash():
    dash_app.run(host="0.0.0.0", port=8050)


if __name__ == "__main__":
    Thread(target=run_api).start()
    Thread(target=run_dash).start()

# notes:
# - this is only for dev
# - for deploying on render, use wsgi.py
