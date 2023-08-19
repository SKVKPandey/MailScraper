import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import sys

# Configure console output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def get_website_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title of the webpage as the name/company
        title = soup.title.string.strip() if soup.title else "No title found"
        return title
    except (requests.exceptions.RequestException, AttributeError):
        return "Error fetching information"

def get_emails_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find email addresses using a regular expression
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        emails = re.findall(email_pattern, soup.get_text())
        return emails
    except (requests.exceptions.RequestException, AttributeError):
        return []

def get_search_results(query, num_results=10):
    search_results = []

    for result in search(query, num_results=num_results):
        search_results.append(result)

    return search_results

search_query = input("Enter your search query: ")
num_results = 100

results = get_search_results(search_query, num_results)
email_list = []
website_info_list = []

for index, url in enumerate(results, start=1):
    emails = get_emails_from_url(url)
    if emails:
        website_info = get_website_info(url)
        website_info_list.append((website_info, url))
        email_list.extend(emails)

print("Websites with emails:")
for index, (website_info, url) in enumerate(website_info_list, start=1):
    print(f"{index}. {website_info} - {url}")

print("List of email addresses:", email_list)

