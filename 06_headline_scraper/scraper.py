import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    """
    Fetch HTML content from the given URL.
    Returns the HTML content as a string or None if there's an error.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def parse_headlines(html):
    """
    Parse HTML content and extract headlines with URLs from Hacker News.
    Returns a list of tuples (title, url) or an empty list if parsing fails.
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Hacker News headlines are in <span class="titleline"> tags
        # The actual headline text is in an <a> tag within the span
        headline_elements = soup.find_all('span', class_='titleline')
        
        headlines = []
        for element in headline_elements:
            link = element.find('a')
            if link and link.text.strip():
                title = link.text.strip()
                url = link.get('href', '')
                
                # Handle relative URLs (for internal HN links)
                if url.startswith('item?'):
                    url = f"https://news.ycombinator.com/{url}"
                
                headlines.append((title, url))
        
        return headlines
    except Exception as e:
        print("Parsing error – structure may have changed")
        return []

def main():
    """
    Main function to fetch and display Hacker News headlines.
    """
    url = "https://news.ycombinator.com/"
    
    print("Fetching headlines from Hacker News...")
    html_content = fetch_html(url)
    
    if html_content is None:
        print("Failed to fetch website content. Please check your internet connection.")
        return
    
    headlines = parse_headlines(html_content)
    
    if not headlines:
        print("No headlines found or parsing failed.")
        return
    
    print(f"\nFound {len(headlines)} headlines:\n")
    for i, (title, url) in enumerate(headlines, 1):
        print(f"{i}. {title}")
        print(f"   Link: {url}\n")

if __name__ == "__main__":
    main()