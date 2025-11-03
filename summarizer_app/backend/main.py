from flask import Flask, request, jsonify
import fitz
from .extract_pdf_text import extract_pdf_text
from .generate_summary import generate_summary

api = Flask(__name__)


@api.route("/extract-text", methods=["POST"])
def extract_text():
    data = request.get_json()

    # validate data
    if not isinstance(data, dict):
        return jsonify({"error": f"input was not a json, was {type(data)}"}), 415  # unsupported media type
    content = data.get("content")
    if content is None:
        return jsonify({"error": "missing field 'content'"}), 400  # Bad request
    if len(data) > 1:
        return jsonify({"error": "unexpected additional JSON fields"}), 400  # Bad request
    if not isinstance(content, str):
        return jsonify({"error": f"content must be of type str, was {type(content)}"}), 415  # unsupported media type
    if not content.startswith("data:application/pdf;"):
        return jsonify({"error": "content must be a 'data:application/pdf;' URI"}), 415  # unsupported media type
    encoding_scheme_data = content.split(";")[1]  # content scheme and following data
    if not encoding_scheme_data.startswith("base64,"):
        return jsonify({"error": "content must be base64-encoded"}), 415  # unsupported media type

    # extract text
    try:
        text = extract_pdf_text(content=content)
        return jsonify({"text": text}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 422  # Bad request
    except fitz.FileDataError as e:
        return jsonify({"error": "Invalid or empty PDF"}), 422  # Unprocessable Entity
    except Exception as e:  # unexpected failure
        return jsonify({"error": "Internal server error"}), 500  # Internal Server Error


@api.route("/summarize-text", methods=["POST"])
def summarize_text():
    data = request.get_json()

    # validate data
    if not isinstance(data, dict):
        return jsonify({"error": f"input was not a json, was {type(data)}"}), 415  # unsupported media type
    text = data.get("text")
    if text is None:
        return jsonify({"error": "missing field 'text'"}), 400  # Bad request
    if len(data) > 1:
        return jsonify({"error": "unexpected additional JSON fields"}), 400  # Bad request
    if not isinstance(text, str):
        return jsonify({"error": f"text must be of type str, was {type(text)}"}), 415  # unsupported media type

    # summarize text
    try:
        summary = generate_summary(text=text)
        return jsonify({"summary": summary}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 422  # Bad request
    except Exception as e:  # unexpected failure
        return (
            jsonify({"error": "Internal server error", "debug": e}),
            500,
        )  # Internal Server Error #TODO: delete "debug" key


if __name__ == "__main__":
    api.run(debug=True)
