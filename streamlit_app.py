import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API URL from .env file
API_URL = os.getenv("API_URL", "http://localhost:5000")  # Default to localhost:5000 if not set


# Get all polls from Flask
def get_all_polls():
    response = requests.get(f"{API_URL}/get_poll")
    if response.status_code == 200:
        return response.json()
    return None


# Submit a vote
def submit_vote(poll_id, option):
    payload = {"poll_id": poll_id, "option": option}
    response = requests.post(f"{API_URL}/vote", json=payload)
    return response.json()


# Create a new poll
def create_poll(question, option_1, option_2):
    payload = {"question": question, "option_1": option_1, "option_2": option_2}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{API_URL}/create_poll", json=payload, headers=headers)

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error("Error parsing server response.")
            return {"message": "Failed to parse response from server"}
    else:
        st.error(f"Error from server: {response.text}")
        return {"message": f"Server returned status code {response.status_code}"}


# Frontend
def main():
    st.title("Voting App")

    # Poll creation section
    st.header("Create a Poll")
    question = st.text_input("Enter your poll question:")
    option_1 = st.text_input("Option 1:")
    option_2 = st.text_input("Option 2:")

    if st.button("Create Poll"):
        if question and option_1 and option_2:
            result = create_poll(question, option_1, option_2)
            st.success(result['message'])
        else:
            st.error("Please fill in all fields.")

    # Fetch all polls
    polls = get_all_polls()

    if polls and isinstance(polls, list) and len(polls) > 0:
        for poll in polls:
            st.header(f"Poll: {poll['question']}")


            # Voting buttons
            option = st.radio("Choose an option", [poll['option_1'], poll['option_2']])

            if st.button(f"Vote on Poll {poll['id']}"):
                vote_response = submit_vote(poll['id'], 'option_1' if option == poll['option_1'] else 'option_2')
                st.write(vote_response['message'])

            # Show current vote counts
            st.write(f"Votes for {poll['option_1']}: {poll['votes_1']}")
            st.write(f"Votes for {poll['option_2']}: {poll['votes_2']}")
    else:
        st.write("No active polls at the moment.")


if __name__ == "__main__":
    main()
