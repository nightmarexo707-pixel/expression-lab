"""Flask web application for Expression Lab."""
import os
from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
from expression_engine import operate, ExpressionError, MAX_EXPRESSION_LENGTH

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # API requests are intentionally small.
ALLOWED_OPERATIONS = {
    "infix_to_postfix", "infix_to_prefix", "postfix_to_infix", "postfix_to_prefix",
    "prefix_to_infix", "prefix_to_postfix", "evaluate_postfix", "evaluate_prefix",
}

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/operate")
def api_operate():
    if not request.is_json:
        return jsonify(success=False, error="Content-Type must be application/json."), 415
    try:
        payload = request.get_json(silent=False)
    except BadRequest:
        return jsonify(success=False, error="Request body must contain valid JSON."), 400
    if not isinstance(payload, dict):
        return jsonify(success=False, error="JSON body must be an object."), 400
    operation = payload.get("operation")
    expression = payload.get("expression")
    if not isinstance(operation, str) or not isinstance(expression, str):
        return jsonify(success=False, error="Both 'operation' and 'expression' must be strings."), 400
    if operation not in ALLOWED_OPERATIONS:
        return jsonify(success=False, error="Unknown operation. Choose one of the supported operations."), 400
    if len(expression) > MAX_EXPRESSION_LENGTH:
        return jsonify(success=False, error=f"Expression is too long (maximum {MAX_EXPRESSION_LENGTH} characters)."), 400
    try:
        result = operate(operation, expression)
        return jsonify(success=True, operation=operation, result=result), 200
    except ExpressionError as exc:
        return jsonify(success=False, operation=operation, error=str(exc)), 400
    except Exception:
        app.logger.exception("Unexpected expression processing failure")
        return jsonify(success=False, error="An unexpected server error occurred. Please try again."), 500

@app.errorhandler(RequestEntityTooLarge)
def request_too_large(_error):
    return jsonify(success=False, error="Request body is too large."), 413

@app.errorhandler(404)
def not_found(_error):
    if request.path.startswith("/api/"):
        return jsonify(success=False, error="API endpoint not found."), 404
    return "Page not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
