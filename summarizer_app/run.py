from wsgi import app

# frontend is available at http://127.0.0.1:8050
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
