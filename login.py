import csv
from flask import jsonify, request

# Function to read users from CSV
def read_users_from_csv():
    users = []
    with open('user.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users.append(row)
    return users

# Login function to validate user credentials from CSV data
def login_user():
    # Get login credentials from the request body
    login_data = request.get_json()
    username = login_data.get("userid")
    password = login_data.get("password")
    print(username)
    print(password)


    # Read users from CSV
    users = read_users_from_csv()

    # Check if the credentials match any user in the CSV data
    user = next((user for user in users if user["userid"] == username and user["password"] == password), None)

    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"error": "Invalid credentials. Please cntact admin for support."}), 401