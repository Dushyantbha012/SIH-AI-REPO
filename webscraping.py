from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

TRUSTED_SITES = [
    "linkedin.com", "indeed.com", "glassdoor.com", "monster.com", "careerbuilder.com",
    "ziprecruiter.com", "remotive.io", "angel.co", "weworkremotely.com", "jobsearch.com",
    "flexjobs.com", "remote.co", "remoteworkers.co", "workingnomads.co", "jobspresso.co",
    "careerjet.com", "simplyhired.com", "jobvite.com", "hired.com", "theladders.com", 
    "techcareers.com", "angel.co/jobs", "gitconnected.com", "upwork.com", "fiverr.com", 
    "toptal.com", "freelancer.com", "monster.ca", "seek.com.au", "reed.co.uk", "jobstreet.com"
]

def fetch_trusted_search_links(query, output_file="trusted_search_links.txt", num_results=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"

    try:
        html = requests.get(url, headers=headers, timeout=10)
        html.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return

    soup = BeautifulSoup(html.text, "html.parser")
    allData = soup.find_all("div", {"class": "g"})
    trusted_links = []

    for i in range(len(allData)):
        link = allData[i].find("a").get("href")
        if link is not None:
            parsed_domain = urlparse(link).netloc.lower()
            if any(trusted_site in parsed_domain for trusted_site in TRUSTED_SITES):
                trusted_links.append(link)

    with open(output_file, "w", encoding="utf-8") as file:
        for link in trusted_links:
            file.write(link + "\n")

    print(f"Trusted links have been saved to '{output_file}'.")

    return trusted_links

if __name__ == "__main__":

    job_type = input("Enter Job Type (internship/private/govt): ").lower()
    role = input("Enter Role: ")
    location = input("Enter Job Location: ")
    years = input("Enter years of experience: ")

    if job_type == "internship":
        query = f"{role} internship with {location} location and {years} of experience required"
    elif job_type == "private":
        query = f"{role} private job with {location} location and {years} of experience required"
    elif job_type == "govt":
        query = f"{role} government job in India with {location} location and {years} of experience required"
    else:
        print("Invalid job type. Please enter 'internship', 'private', or 'govt'.")
        exit(1)

    t = fetch_trusted_search_links(query, num_results=100)
    print(t)


