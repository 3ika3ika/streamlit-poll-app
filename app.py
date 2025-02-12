from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database connection using environment variables
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),  # Database host from .env
        user=os.getenv("DB_USER"),  # Database user from .env
        password=os.getenv("DB_PASSWORD"),  # Database password from .env
        database=os.getenv("DB_NAME")  # Database name from .env
    )

@app.route('/')
def home():
    return "Welcome to the Voting App!"

# Get current poll details
@app.route('/get_poll', methods=['GET'])
def get_poll():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM polls ORDER BY id DESC LIMIT 1")
    poll = cursor.fetchone()
    conn.close()

    if poll:
        return jsonify(poll)
    return jsonify({"message": "No active poll"})


# Create a new poll
@app.route('/create_poll', methods=['POST'])
def create_poll():
    data = request.json
    question = data.get('question')
    option_1 = data.get('option_1')
    option_2 = data.get('option_2')

    # Ensure that all fields are filled out
    if not question or not option_1 or not option_2:
        return jsonify({"message": "Invalid input, all fields are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO polls (question, option_1, option_2, votes_1, votes_2) VALUES (%s, %s, %s, %s, %s)",
            (question, option_1, option_2, 0, 0)  # Initial votes set to 0
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Poll created successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Vote for an option
@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    poll_id = data.get('poll_id')
    option = data.get('option')

    if not poll_id or option not in ['option_1', 'option_2']:
        return jsonify({"message": "Invalid input"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Update vote count
    if option == 'option_1':
        cursor.execute(f"UPDATE polls SET votes_1 = votes_1 + 1 WHERE id = {poll_id}")
    elif option == 'option_2':
        cursor.execute(f"UPDATE polls SET votes_2 = votes_2 + 1 WHERE id = {poll_id}")

    conn.commit()
    conn.close()

    return jsonify({"message": "Vote recorded successfully"})


if __name__ == '__main__':
    app.run(debug=True)
