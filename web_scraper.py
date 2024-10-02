import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all text from the page
        text_content = soup.get_text(separator=' ', strip=True)
        
        return text_content
    else:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

def scrape_all_pages(base_url):
    visited_urls = set()
    to_visit = [base_url]
    all_text = []

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited_urls:
            continue

        print(f"Scraping: {current_url}")
        text_content = scrape_website(current_url)
        all_text.append(text_content)
        visited_urls.add(current_url)

        # Find all links on the current page
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urllib.parse.urljoin(base_url, href)
            if full_url.startswith(base_url) and full_url not in visited_urls:
                to_visit.append(full_url)

    return "\n\n".join(all_text)

if __name__ == "__main__":
    website_url = input("Enter the website URL to scrape: ")
    scraped_content = scrape_all_pages(website_url)
    
    # Save the scraped content to a file
    with open("scraped_content.txt", "w", encoding="utf-8") as f:
        f.write(scraped_content)
    
    print("Scraping completed. Content saved to 'scraped_content.txt'")
