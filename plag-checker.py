import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.gowinston.ai/v2/ai-content-detection"

payload = {
    "text": "Hi, I am Dushyant Bhardwaj. I am a second year undergrad at Punjab Engineering College, Chandigarh. I live in Faridabad. I enjoy making web applications using frameworks such as ReactJS and NextJS. I have made advanced projects, which include a job platform which automates the hiring process and a clone of Discord which is also known as Piscord.",
    "version": "latest",
    "sentences": True,
    "language": "en"
}
headers = {
    "Authorization": f"Bearer {os.environ["GOWINSTON_API_TOKEN"]}",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)