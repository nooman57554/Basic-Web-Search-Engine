# Basic Web Search Engine

This project is a basic web search engine that crawls web pages, calculates PageRank, and provides search functionality using TF-IDF and cosine similarity.

## Features

- **Web Crawler:** Extracts content and links from web pages using BeautifulSoup and Selenium.
- **PageRank Calculation:** Computes PageRank using a directed graph (NetworkX).
- **Search Engine:** Implements TF-IDF and cosine similarity for relevance-based search.
- **Web Interface:** Simple web interface built with Flask for user queries.

## Tech Stack

- **Programming Language:** Python
- **Libraries and Frameworks:**
  - Flask (for web application)
  - SQLAlchemy (for database ORM)
  - BeautifulSoup (for web scraping)
  - Selenium (for dynamic content scraping)
  - NetworkX (for PageRank calculation)
  - Scikit-learn (for TF-IDF and cosine similarity)
- **Database:** SQLite
- **Frontend:** HTML, CSS

## Project Structure

```
.
├── web_crawler.py      # Web crawling and data storage
├── pagerank.py         # PageRank calculation
├── websearch.py        # Flask application for search engine
├── templates/          # HTML templates
│   ├── homepage.html   # Homepage for search input
│   └── results.html    # Displays search results
│   └── styles.css      # CSS for styling
├── crawler.db          # SQLite database
└── README.md           # Project documentation
```

## Setup and Usage

### Prerequisites

- Python 3.8+
- Google Chrome browser
- ChromeDriver (matching the installed Chrome version)
- Install required Python libraries:

  ```bash
  pip install -r requirements.txt
  ```

### Running the Project

1. **Initialize Database:**
   - Ensure `crawler.db` exists or is created by running the crawler as shown in below step 2.

2. **Run Web Crawler:**
   ```bash
   python web_crawler.py
   ```
   Adjust the number of pages to crawl by modifying the `webcrawler` function.

3. **Calculate PageRank:**
   ```bash
   python pagerank.py
   ```

4. **Start the Flask Application:**
   ```bash
   python websearch.py
   ```
   Access the application at `http://127.0.0.1:5000/`.

5. **Search for Content:**
   - Enter your query on the homepage to see ranked search results.

## Screenshots

### Homepage
![Homepage](static/Screenshot%20(113).png)

### Search Results
![Search Results](static/Screenshot%20(114).png)

## Future Improvements

- Add support for advanced search operators.
- Implement crawling rate limiting and error handling.
- Expand frontend with AJAX for instant search suggestions.
- Optimize TF-IDF weighting and scoring.



---

Contributions and suggestions are welcome! 🚀
