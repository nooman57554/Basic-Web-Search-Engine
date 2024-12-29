from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine, Column, String, Text, Integer, Float, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

Base = declarative_base()
engine = create_engine("sqlite:///crawler.db")

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String)
    content = Column(Text)
    outgoing_links = Column(JSON)
    pagerank = Column(Float, default=1.0)

Base.metadata.create_all(engine)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def webcrawler(no_of_pages):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Setup headless browser
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    #seed_urls = ["https://www.bbc.com","https://www.discovery.com/"]
    seed_urls = ["https://dictionary.cambridge.org/"]
    
    visited_urls = set()

    for url in seed_urls:
        queue = [url]
        pages_crawled = 0 

        while queue and pages_crawled < no_of_pages:
            url = queue.pop(0)

            if url in visited_urls:
                continue
            
            outgoing_links = []

            try:
                # Extract content
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                title = soup.title.string if soup.title else 'No title'

                # Remove unwanted sections
                for tag in soup(['header', 'footer', 'nav', 'aside', 'script', 'style']):
                    tag.decompose()

                # Extract meaningful content
                main_content = ""
                try:
                    # Target <article>, <p>, or specific divs likely to contain content
                    article = soup.find('article')
                    if article:
                        main_content = article.get_text(separator="\n", strip=True)
                    else:
                        # Fallback to paragraphs if <article> is not found
                        paragraphs = soup.find_all('p')
                        main_content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

                    # Limit content length to avoid storing too much irrelevant data
                    if len(main_content) > 2000:  # Adjust length as needed
                        main_content = main_content[:2000] + "..."
                except Exception as e:
                    print(f"Error extracting content from {url}: {e}")

                visited_urls.add(url)
                
                # Extract links
                for link in soup.find_all('a'):
                    href = link.get("href")
                    if href and href.startswith("http"):
                        if href not in visited_urls:
                            queue.append(href)
                        outgoing_links.append(href)

                # Add to database
                page = Page(
                    url=url,
                    title=title,
                    content=main_content,
                    outgoing_links=outgoing_links,
                    pagerank=1.0
                )

                session.add(page)
                session.commit()

                pages_crawled += 1
                print(f"Crawled: {url}")
                print(f"Title: {title}")
                print(f"Content Preview: {main_content[:200]}")
            
            except Exception as e:
                print(f"Failed to crawl {url}: {e}")
        
        driver.quit()
        print("Crawling complete.")

if __name__ == "__main__":
    webcrawler(no_of_pages= 50)
