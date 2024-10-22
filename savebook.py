from flask import Blueprint, request, jsonify
import pandas as pd
import os
from datetime import datetime
import pytz

# Create a Flask Blueprint for the controller
controller = Blueprint('controller', __name__)

# Function to save the book data to the CSV file
def save_book(data):
    # Define the CSV file path
    csv_file = 'mybook.csv'

    # Get the current date and time in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

    # Add the current datetime to the incoming data
    data['datetime'] = current_time

    # Create the DataFrame from the incoming data
    new_data = pd.DataFrame([data])

    # Check if the CSV file exists
    if os.path.exists(csv_file):
        # Read the existing CSV file into a DataFrame
        existing_data = pd.read_csv(csv_file)

        # Check for duplicates
        if ((existing_data['author'] == data['author']) &
                (existing_data['booktitle'] == data['book']) &
                (existing_data['userid'] == data['userid'])).any():
            return {"error": "Book already in your list."}

        # Append the new data to the existing CSV file
        new_data.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        # If the file doesn't exist, create it and write the header
        new_data.to_csv(csv_file, mode='w', header=True, index=False)
