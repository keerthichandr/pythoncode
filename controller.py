from flask import Flask, jsonify, request
from login import login_user
from search import recommend_books
from savebook import save_book
from mybook import get_mybook

app = Flask(__name__)

def add_cors_headers(response):
    """Add CORS headers to the response."""
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'  # Allowed methods
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allowed headers
    return response

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    """Login endpoint."""
    if request.method == 'OPTIONS':
        return add_cors_headers(jsonify({})), 200  # Handle preflight request

    response = login_user()  # This should return a tuple (response, status_code)

    # Ensure response is a valid Flask response
    if isinstance(response, tuple):
        response_body, status_code = response
    else:
        response_body = response
        status_code = 200  # Default status code if not provided

    return add_cors_headers(response_body), status_code  # Return modified response with status code

@app.route('/api/search', methods=['GET', 'OPTIONS'])
def get_recommendations():
    """Get book recommendations based on a description."""
    if request.method == 'OPTIONS':
        return add_cors_headers(jsonify({})), 200  # Handle preflight request

    description = request.args.get('description')

    if not description:
        response_body = jsonify({"error": "Missing 'description' parameter"})
        return add_cors_headers(response_body), 400

    recommendations = recommend_books(description)
    response_body = jsonify({"recommendations": recommendations})
    return add_cors_headers(response_body), 200

@app.route('/api/mybooks', methods=['GET', 'OPTIONS'])
def get_stored_books():
    """Get stored books for a specific user."""
    if request.method == 'OPTIONS':
        return add_cors_headers(jsonify({})), 200  # Handle preflight request

    userid = request.args.get('userid')

    if not userid:
        response_body = jsonify({"error": "User ID is required."})
        return add_cors_headers(response_body), 400

    recommendations = get_mybook(userid)

    if recommendations is None:
        response_body = jsonify({"error": "User ID is required."})
        return add_cors_headers(response_body), 400
    if not recommendations:
        response_body = jsonify({"error": "No books found for the provided User ID."})
        return add_cors_headers(response_body), 404

    response_body = jsonify({"recommendations": recommendations})
    return add_cors_headers(response_body), 200

@app.route('/api/save', methods=['POST', 'OPTIONS'])
def save():
    """Save book data."""
    if request.method == 'OPTIONS':
        return add_cors_headers(jsonify({})), 200  # Handle preflight request

    data = request.get_json()

    required_fields = ['author', 'book', 'userid']
    if not all(field in data for field in required_fields):
        response = jsonify({"error": "Missing required fields"})
        if isinstance(response, tuple):
            response_body, status_code = response
        else:
            response_body = response

        return add_cors_headers(response_body), 400

    result = save_book(data)
    if result is None:
        response = jsonify({"message": "Book data saved successfully!"})
        if isinstance(response, tuple):
            response_body, status_code = response
        else:
            response_body = response
        return add_cors_headers(response_body), 201

    if "error" in result:
        response = jsonify(result)
        if isinstance(response, tuple):
            response_body, status_code = response
        else:
            response_body = response

        return add_cors_headers(response_body), 400  # Return error response with CORS headers

# Apply CORS headers to all responses
@app.after_request
def after_request(response):
    """Apply CORS headers after each request."""
    return add_cors_headers(response)


