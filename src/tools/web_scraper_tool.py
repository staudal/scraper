import requests
from bs4 import BeautifulSoup
from typing import TypedDict
from src.config import BATCH_SIZE

class WebBatch(TypedDict):
    id: str
    content: str
    url: str

class WebsiteData:
    def __init__(self, url: str, batch_size: int = None):
        self.url = url
        self.batch_size = batch_size or BATCH_SIZE
        self.words = []
        self.current_batch = 0
        self._scrape_website()
    
    def _scrape_website(self):
        """Scrape the website and prepare words for batching"""
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content
            text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            self.words = text.split()

        except Exception as e:
            raise ValueError(f"Failed to scrape website: {str(e)}")

    def get_next_batch(self) -> WebBatch:
        """Get the next batch of content"""
        start_idx = self.current_batch * self.batch_size
        end_idx = start_idx + self.batch_size

        if start_idx >= len(self.words):
            raise ValueError("No more batches available")

        batch_words = self.words[start_idx:end_idx]
        batch_content = ' '.join(batch_words)

        self.current_batch += 1

        return WebBatch({
            'id': str(self.current_batch),
            'content': batch_content,
            'url': self.url
        })

    def has_next_batch(self) -> bool:
        """Check if there are more batches available"""
        return self.current_batch * self.batch_size < len(self.words)

def initialize_website_scraper(url: str, batch_size: int = None) -> str:
    """Initialize website scraper and return a session ID"""
    global _website_sessions
    if '_website_sessions' not in globals():
        _website_sessions = {}

    session_id = f"session_{len(_website_sessions) + 1}"
    _website_sessions[session_id] = WebsiteData(url, batch_size or BATCH_SIZE)
    return session_id

def get_next_batch(session_id: str) -> WebBatch:
    """Get the next batch from a scraping session"""
    global _website_sessions
    if '_website_sessions' not in globals() or session_id not in _website_sessions:
        raise ValueError(f"Invalid session ID: {session_id}")

    return _website_sessions[session_id].get_next_batch()
    
def has_more_batches(session_id: str) -> bool:
    """Check if there are more batches in the session"""
    global _website_sessions
    if '_website_sessions' not in globals() or session_id not in _website_sessions:
        raise ValueError(f"Invalid session ID: {session_id}")
    
    return _website_sessions[session_id].has_next_batch()