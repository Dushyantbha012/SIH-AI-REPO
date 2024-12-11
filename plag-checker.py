import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.gowinston.ai/v2/ai-content-detection"

payload = {
    "text": "Rain is a natural phenomenon where water droplets form in clouds and fall to the ground due to gravity. It is a vital part of the Earth's water cycle, replenishing freshwater sources and sustaining ecosystems. Rain cools the air, nourishes plants, and supports agriculture, making it essential for life. It can vary from gentle drizzles to heavy downpours, each having its impact on the environment and human activities. While rain is often welcomed for its life-giving properties, excessive rainfall can lead to flooding and other natural disasters. Its rhythmic sound and earthy aroma often evoke feelings of calmness and renewal.",
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