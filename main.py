"""
This module provides functionality for scraping Google Scholar, analyzing the scraped URLs, and downloading the associated PDFs.

The main functionality is provided by the `main()` function, which performs the following steps:

1. Prompts the user for a search query and the maximum number of results to scrape.
2. Scrapes the top `max_results` URLs from Google Scholar for the given search query.
3. Analyzes the scraped URLs, extracting metadata such as title, author, publication date, and PDF links.
4. Allows the user to download the PDFs for the scraped URLs.
5. Generates a log file with the extracted metadata.

The module also includes utility functions for setting up a SQLite database to store the scraped URLs, saving the URLs to the database, and generating the log file.
"""
import sqlite3
from datetime import datetime
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
import os

# Database setup
DB_FILE = "../scraped_urls.db"
LOG_FILE = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"


def setup_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    search_query TEXT,
                    url TEXT,
                    scraped_on DATETIME DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()


def save_url_to_db(search_query, urls):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for url in urls:
        c.execute("INSERT INTO urls (search_query, url) VALUES (?, ?)", (search_query, url))
    conn.commit()
    conn.close()


# 1. User Input for Search Query
def get_user_input():
    query = input("Enter your search query: ")
    max_results = int(input("Enter the number of results to scrape: "))
    return query, max_results


# 2. Scrape Google Scholar
def scrape_google_scholar(query, max_results):
    print("Scraping Google Scholar...")
    urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        search_url = f"https://scholar.google.com/scholar?q={query.replace(' ', '+')}"
        page.goto(search_url)

        # Extract URLs
        links = page.eval_on_selector_all(
            "h3.gs_rt a",
            "elements => elements.map(el => el.href)"
        )
        urls.extend(links[:max_results])
        browser.close()

    print(f"Found {len(urls)} URLs.")
    return urls


# 3. Analyze Websites
def analyze_urls(urls):
    print("Analyzing URLs...")
    metadata = []
    for url in urls:
        print(f"Processing: {url}")
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract Metadata
            title = soup.title.string if soup.title else "No Title"
            author = soup.find("meta", attrs={"name": "author"})
            author = author["content"] if author else "Unknown Author"
            publication_date = soup.find("meta", attrs={"name": "date"})
            publication_date = publication_date["content"] if publication_date else "Unknown Date"

            # Find PDF Links
            pdf_link = None
            for a_tag in soup.find_all("a", href=True):
                if ".pdf" in a_tag["href"]:
                    pdf_link = a_tag["href"]
                    break

            metadata.append({
                "url": url,
                "title": title,
                "author": author,
                "date": publication_date,
                "pdf_link": pdf_link
            })
        except Exception as e:
            print(f"Error processing {url}: {e}")
            metadata.append({"url": url, "error": str(e)})

    return metadata


# 4. Ask User to Download PDFs
def download_pdfs(metadata):
    download_choice = input("Do you want to download the PDFs? (1 for yes, 0 for no): ")
    if download_choice != "1":
        return

    os.makedirs("pdfs", exist_ok=True)
    for item in metadata:
        if "pdf_link" in item and item["pdf_link"]:
            try:
                response = requests.get(item["pdf_link"], stream=True)
                file_name = os.path.join("pdfs", item["pdf_link"].split("/")[-1])
                with open(file_name, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print(f"Downloaded: {file_name}")
            except Exception as e:
                print(f"Failed to download {item['pdf_link']}: {e}")


# 5. Generate Log
def generate_log(metadata):
    with open(LOG_FILE, "w") as log_file:
        for item in metadata:
            log_file.write(f"URL: {item.get('url', 'N/A')}\n")
            log_file.write(f"Title: {item.get('title', 'N/A')}\n")
            log_file.write(f"Author: {item.get('author', 'N/A')}\n")
            log_file.write(f"Date: {item.get('date', 'N/A')}\n")
            log_file.write(f"PDF Link: {item.get('pdf_link', 'N/A')}\n")
            log_file.write("\n")
    print(f"Log saved to {LOG_FILE}")


# Main Function
def main():
    setup_database()

    # Step 1: User Input
    query, max_results = get_user_input()

    # Step 2: Scrape Google Scholar
    urls = scrape_google_scholar(query, max_results)
    save_url_to_db(query, urls)

    # Step 3: Analyze URLs
    metadata = analyze_urls(urls)

    # Step 4: Download PDFs
    download_pdfs(metadata)

    # Step 5: Generate Log
    generate_log(metadata)


if __name__ == "__main__":
    main()