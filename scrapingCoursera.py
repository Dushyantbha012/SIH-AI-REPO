import base64
import requests
from urllib.parse import quote
import os
from dotenv import load_dotenv

load_dotenv()

# Replace these with your actual credentials
APP_KEY = os.environ["COURSERA_CLIENT_ID"]
APP_SECRET = os.environ["COURSERA_CLIENT_SECRET"]

def get_access_token(app_key, app_secret):
    # Base64 encode the "key:secret" string
    credentials = f"{app_key}:{app_secret}".encode("utf-8")
    b64_credentials = base64.b64encode(credentials).decode("utf-8")

    url = "https://api.coursera.com/oauth2/client_credentials/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64_credentials}"
    }
    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        raise Exception(f"Failed to obtain access token: {response.status_code}, {response.text}")

def search_courses(access_token, query="Data Science", limit=5):
    search = quote(query)
    api_url = "https://api.coursera.org/api/courses.v1"
    params = {
        "q": "search",
        "query": search,
        "limit": limit
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to search courses: {response.status_code}, {response.text}")

if __name__ == "__main__":
    try:
        # Step 1: Obtain Access Token
        access_token = get_access_token(APP_KEY, APP_SECRET)
        print("Access token obtained successfully.\n")

        # Step 2: Search for courses
        query = "data analysis"
        limit = 5
        print(f"Searching for courses with query: '{query}'...\n")
        courses_data = search_courses(access_token, query=query, limit=limit)

        # Display retrieved courses
        elements = courses_data.get("elements", [])
        if elements:
            print("Courses Found:\n")
            for course in elements:
                name = course.get("name", "N/A")
                slug = course.get("slug", "N/A")
                print(f"{name}: https://coursera.org/learn/{slug}")
        else:
            print("No courses found for the given query.")

    except Exception as e:
        print("Error:", str(e))