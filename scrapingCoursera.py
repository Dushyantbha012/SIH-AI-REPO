import requests
from dotenv import load_dotenv
import os
from urllib.parse import quote

load_dotenv()

search = "NLP"
limit = 10
search2 = quote(search)

print("Search2:", search2)

# Define the API endpoint and your access token
url = f"https://api.coursera.org/api/courses.v1?q=search&query={search2}&limit={limit}"
headers = {
    "Authorization": f"Bearer {os.environ['COURSERA_API_KEY']}",
}

# Make the GET request
response = requests.get(url, headers=headers)

# Parse the JSON response
if response.status_code == 200:
    data = response.json()
    print(data['elements'])  # Full response for inspection
else:
    print(f"Error: {response.status_code}, {response.text}")