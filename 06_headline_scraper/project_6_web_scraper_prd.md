
# Project 6: Web Scraper (Intro to Libraries) - PRD

## 1. Overview
This project involves creating a Python script that scrapes article headlines from a website (e.g., Hacker News) and prints them to the console. This will introduce you to external libraries and web scraping fundamentals.

## 2. Functional Requirements
- **Fetch HTML Content:** Use the `requests` library to retrieve HTML from the target URL.
- **Parse HTML:** Use the `BeautifulSoup` class from `beautifulsoup4` to parse HTML content.
- **Extract Headlines:** Identify the HTML tag and class containing article headlines and extract them into a list.
- **Display Output:** Print extracted headlines as a numbered list to the console.
- **Error Handling:**
  - Handle `requests` exceptions for connectivity issues.
  - Handle parsing errors gracefully (e.g., if the HTML structure changes).

## 3. Non-functional Requirements
- Code must be modular with at least three functions: `fetch_html(url)`, `parse_headlines(html)`, and `main()`.
- All external library imports must be at the top of the file.
- The script must include comments indicating which sections were assisted by Claude.
- The output must be human-readable and numbered.

## 4. User Stories
- **As a user**, I want to see a list of article headlines from a website so I can quickly know the latest articles.
- **As a developer**, I want modular and maintainable code so I can reuse the scraping logic for other websites.

## 5. Acceptance Criteria
- Given internet access, running the script prints at least 10 article headlines to the console.
- If the website is unreachable, the script prints an error message without crashing.
- If parsing fails, the script prints “Parsing error – structure may have changed” without crashing.
- The script must run using `python scraper.py` in a terminal.

## 6. Constraints
- The script must work with Python 3.8+.
- Only standard Python libraries and `requests`/`beautifulsoup4` are allowed.
- Target site should be a publicly accessible site without login.

## 7. Deliverables
- `scraper.py` Python file.
- Screenshot of successful execution in terminal showing headlines.
- Requirements file (`requirements.txt`) listing `requests` and `beautifulsoup4`.

## 8. Lessons Learned
- HTTP request/response basics.
- HTML structure navigation and parsing.
- Using external Python packages.
- Structuring code for maintainability.

