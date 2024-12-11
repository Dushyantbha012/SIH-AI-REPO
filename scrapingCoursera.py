import requests
import webbrowser
from flask import Flask, request
import os

# Configuration
CLIENT_ID = os.environ["COURSERA_CLIENT_ID"]
CLIENT_SECRET = os.environ["COURSERA_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = "view-profile"

# Flask app for handling the redirect
app = Flask(__name__)
authorization_code = None

@app.route("/callback")
def callback():
    global authorization_code
    authorization_code = request.args.get("code")
    return "Authorization code received! You can return to the terminal."

# Step 1: Generate Authorization URL
def generate_auth_url():
    auth_url = (
        f"https://accounts.coursera.org/oauth2/v1/auth?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}"
    )
    return auth_url

# Step 2: Exchange Authorization Code for Access Token
def get_access_token(code):
    token_url = "https://accounts.coursera.org/oauth2/v1/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get access token: {response.status_code}, {response.text}")

# Step 3: Fetch Courses
def fetch_courses(access_token, query="Data Science", limit=5):
    api_url = f"https://api.coursera.org/api/courses.v1?q=search&query={query}&limit={limit}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch courses: {response.status_code}, {response.text}")

if __name__ == "__main__":
    try:
        # Step 1: Generate and Open Authorization URL
        auth_url = generate_auth_url()
        print("Opening browser for authorization...\n")
        print(f"If the browser doesn't open, go to this URL: {auth_url}\n")
        webbrowser.open(auth_url)

        # Step 2: Start Flask App to Capture Authorization Code
        print("Starting Flask server to capture authorization code...")
        app.run(port=5000)

        # Step 3: Wait for Authorization Code
        if authorization_code:
            print(f"Authorization Code: {authorization_code}\n")

            # Exchange Authorization Code for Access Token
            print("Exchanging authorization code for access token...")
            access_token = get_access_token(authorization_code)
            print(f"Access Token: {access_token}\n")

            # Fetch Courses
            print("Fetching courses from Coursera API...")
            courses = fetch_courses(access_token, query="Data Science", limit=5)
            print("Courses:", courses)

    except Exception as e:
        print("Error:", str(e))