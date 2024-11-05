import requests
from bs4 import BeautifulSoup
import os
import re


def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Create the base folder for the website
    folder_name = f"templates/{url.split('//')[-1].replace('/', '_')}"
    os.makedirs(f"{folder_name}/css", exist_ok=True)
    os.makedirs(f"{folder_name}/js", exist_ok=True)
    os.makedirs(f"{folder_name}/images", exist_ok=True)

    # Save HTML content
    with open(f"{folder_name}/index.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

    # Fetch linked resources
    fetch_resources(soup, folder_name, url)

    return folder_name


def fetch_resources(soup, folder_name, base_url):
    # Extract and download CSS
    for css in soup.find_all("link", {"rel": "stylesheet"}):
        css_url = css.get("href")
        if css_url:
            save_resource(css_url, f"{folder_name}/css", base_url)

    # Extract and download JS
    for script in soup.find_all("script"):
        js_url = script.get("src")
        if js_url:
            save_resource(js_url, f"{folder_name}/js", base_url)

    # Extract and download Images
    for img in soup.find_all("img"):
        img_url = img.get("src")
        if img_url:
            save_resource(img_url, f"{folder_name}/images", base_url)


def save_resource(resource_url, folder_path, base_url):
    if not resource_url.startswith("http"):
        resource_url = base_url + resource_url

    # Sanitize filename by removing invalid characters
    filename = resource_url.split("/")[-1]
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)  # Replace invalid characters with underscores

    response = requests.get(resource_url)
    with open(f"{folder_path}/{filename}", "wb") as file:
        file.write(response.content)
