import subprocess
import sys

def start_flask():
    # Run Flask app in a separate process
    flask_process = subprocess.Popen([sys.executable, 'app.py'])
    return flask_process

def start_streamlit():
    # Run Streamlit app in a separate process
    streamlit_process = subprocess.Popen(['streamlit', 'run', 'streamlit_app.py'])
    return streamlit_process

if __name__ == "__main__":
    # Start Flask backend
    flask_process = start_flask()

    # Start Streamlit frontend
    streamlit_process = start_streamlit()

    try:
        # Keep both processes running
        flask_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        # Ensure to terminate both processes when you stop the script
        flask_process.terminate()
        streamlit_process.terminate()
