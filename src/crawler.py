import threading
import requests
import json
import csv
import time
import random
import logging
from bs4 import BeautifulSoup
from collections import deque
from datetime import datetime
from urllib.parse import urljoin, urlparse
from pathlib import Path
from fake_useragent import UserAgent
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CrawlerConfig:
    def __init__(self, config_file='config/selectors.json'):
        self.selectors = self._load_selectors(config_file)
        self.ua = UserAgent()

    def _load_selectors(self, path):
        try:
            with open(path, 'r') as f:
                return json.load(f).get('default', {})
        except FileNotFoundError:
            return {}

class RobustCrawler:
    def __init__(self, start_url, max_depth=2, delay=1.0, callback=None):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.max_depth = max_depth
        self.delay = delay
        self.callback = callback
        
        self.config = CrawlerConfig()
        self.queue = deque([(start_url, 0)])
        self.visited = set([start_url])
        self.results = []
        self.is_running = False
        
        # Statistics
        self.stats = {'scanned': 0, 'products_found': 0, 'errors': 0}

    def get_headers(self):
        return {
            'User-Agent': self.config.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }

    def extract_data(self, soup, url):
        data = {'url': url}
        found_any = False
        
        for field, selectors in self.config.selectors.items():
            data[field] = "N/A"
            for selector in selectors:
                try:
                    element = soup.select_one(selector)
                    if element:
                        text = element.get_text(strip=True)
                        if text:
                            data[field] = text
                            found_any = True
                            break
                except Exception:
                    continue
        
        return data if found_any else None

    def crawl_step(self):
        if not self.queue or not self.is_running:
            return False

        url, depth = self.queue.popleft()
        
        if depth > self.max_depth:
            return True # Skip deep but continue queue

        try:
            self.stats['scanned'] += 1
            if self.callback:
                self.callback('status', f"Scanning: {url[:60]}...")

            response = requests.get(url, headers=self.get_headers(), timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Extract Product
                product = self.extract_data(soup, url)
                if product:
                    self.results.append(product)
                    self.stats['products_found'] += 1
                    if self.callback:
                        self.callback('data', product)

                # Discover Links
                if depth < self.max_depth:
                    for a in soup.find_all('a', href=True):
                        link = urljoin(url, a['href'])
                        parsed = urlparse(link)
                        
                        # Stay on same domain and avoid common non-content extensions
                        if parsed.netloc == self.base_domain and link not in self.visited:
                            if not any(link.lower().endswith(ext) for ext in ['.png', '.jpg', '.css', '.js', '.pdf']):
                                self.visited.add(link)
                                self.queue.append((link, depth + 1))

            time.sleep(self.delay + random.uniform(0, 0.5))
            
        except Exception as e:
            self.stats['errors'] += 1
            logging.error(f"Error on {url}: {e}")

        return True

    def start(self):
        self.is_running = True
        while self.is_running and self.queue:
            self.crawl_step()
        
        if self.callback:
            self.callback('done', self.stats)

    def stop(self):
        self.is_running = False

    def export_data(self, format='csv', filename='output'):
        df = pd.DataFrame(self.results)
        if df.empty:
            return False, "No data to export"
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{filename}_{timestamp}.{format}"
        
        try:
            if format == 'csv':
                df.to_csv(path, index=False)
            elif format == 'json':
                df.to_json(path, orient='records', indent=2)
            elif format == 'xlsx':
                df.to_excel(path, index=False)
            return True, path
        except Exception as e:
            return False, str(e)
