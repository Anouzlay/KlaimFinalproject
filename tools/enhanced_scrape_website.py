import streamlit as st
import requests
from bs4 import BeautifulSoup
import logging
import time
from io import BytesIO
import io
import re
import random
import json
from urllib.parse import urlparse
from typing import Any


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# def scrape_website(url, javascript=False, wait_time=3, max_retries=2, timeout=30, global_timeout=180):
#     global _scrape_cache
#     if url in _scrape_cache:
#         print(f"Using cached scrape results for: {url}")
#         return _scrape_cache[url]
    

    
#     # Initialize the global timeout tracker
#     start_time = time.time()
    
#     def check_global_timeout():
#         """Check if the global timeout has been exceeded"""
#         elapsed = time.time() - start_time
#         if elapsed > global_timeout:
#             print(f"Global timeout exceeded ({global_timeout}s). Stopping scrape process.")
#             raise TimeoutError(f"Global scraping timeout exceeded ({global_timeout}s)")
#         return elapsed
    
#     is_pdf = url.lower().endswith('.pdf')
    
#     user_agents = [
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
#         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
#         'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
#     ]
#     headers = {
#         'User-Agent': random.choice(user_agents),
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Referer': 'https://www.google.com/',
#         'DNT': '1',
#         'Connection': 'keep-alive',
#         'Upgrade-Insecure-Requests': '1',
#         'Cache-Control': 'max-age=0',
#     }
    
#     def get_domain(url):
#         parsed_uri = urlparse(url)
#         return '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    
#     def clean_text(text):
#         """Clean up extracted text"""
#         if not text:
#             return ""
#         text = re.sub(r'\s+', ' ', text)
#         text = re.sub(r'\n+', '\n', text)
#         text = '\n'.join(line for line in text.splitlines() if line.strip())
#         return text
    
#     def extract_content(html_content):
#         # Check global timeout before processing
#         check_global_timeout()
        
#         soup = BeautifulSoup(html_content, 'html.parser')
        
#         result = {
#             "title": "",
#             "all_text": "",
#             "main_content": "",
#             "links": [],
#             "structured_data": {},
#             "metadata": {},
#             "html": html_content  
#         }
        
#         if soup.title:
#             result["title"] = soup.title.get_text(strip=True)
        
#         meta_desc = soup.find('meta', attrs={'name': 'description'})
#         if meta_desc and meta_desc.get('content'):
#             result["metadata"]["description"] = meta_desc.get('content')

#         for element in soup.select('script, style'):
#             element.decompose()
        
#         result["all_text"] = clean_text(soup.get_text(separator='\n', strip=True))
        
#         main_content_selectors = ['main', '#content', '.content', 'article', '.article', '.post', '#main', '.main-content']
#         for selector in main_content_selectors:
#             content_elements = soup.select(selector)
#             if content_elements:
#                 content = '\n'.join(element.get_text(separator='\n', strip=True) for element in content_elements)
#                 if len(content) > 200: 
#                     result["main_content"] = clean_text(content)
#                     break
        
#         if not result["main_content"]:
#             result["main_content"] = result["all_text"]
        
#         for link in soup.find_all('a', href=True):
#             href = link.get('href')
#             text = link.get_text(strip=True)
#             if href and not href.startswith('#') and not href.startswith('javascript:'):
#                 result["links"].append({
#                     "url": href,
#                     "text": text
#                 })
        
#         jsonld_elements = soup.select('script[type="application/ld+json"]')
#         if jsonld_elements:
#             structured_json = []
#             for jsonld in jsonld_elements:
#                 try:
#                     if jsonld.string:
#                         json_data = json.loads(jsonld.string)
#                         structured_json.append(json_data)
#                 except Exception as e:
#                     logger.warning(f"Error parsing JSON-LD: {str(e)}")
            
#             if structured_json:
#                 result["structured_data"]["json_ld"] = structured_json
        
#         return result
    
#     def extract_pdf_content(pdf_bytes):
#         # Check global timeout before processing
#         check_global_timeout()
        
#         # Rest of PDF extraction code...
#         # (PDF extraction code omitted for brevity - use your original code here)
#         pass
    
#     # Modified request method with retry logic and global timeout
#     def try_requests_method(current_retry=0):
#         # Check global timeout before attempting
#         elapsed = check_global_timeout()
        
#         if current_retry >= max_retries:
#             logger.warning(f"Exceeded maximum retries ({max_retries}) for standard requests method")
#             raise Exception(f"Exceeded maximum retries ({max_retries})")
        
#         # Calculate remaining time for this request
#         remaining_time = min(timeout, global_timeout - elapsed)
#         if remaining_time <= 0:
#             raise TimeoutError("Global timeout exceeded during requests attempt")
            
#         try:
#             current_headers = headers.copy()
#             current_headers['Referer'] = get_domain(url)
            
#             # Add a progress indicator
#             with st.spinner(f"Attempting standard request (try {current_retry+1}/{max_retries}, {remaining_time:.1f}s remaining)..."):
#                 session = requests.Session()
#                 response = session.get(
#                     url, 
#                     headers=current_headers, 
#                     timeout=remaining_time,  # Use the remaining time as timeout
#                     allow_redirects=True
#                 )
#                 response.raise_for_status()
                
#                 # Check global timeout again before processing response
#                 check_global_timeout()
                
#                 content_type = response.headers.get('Content-Type', '').lower()
                
#                 if 'application/pdf' in content_type or is_pdf:
#                     return extract_pdf_content(response.content)
#                 elif 'application/json' in content_type:
#                     return {"json_data": response.json(), "method": "requests_json"}
#                 elif 'text/html' in content_type or 'application/xhtml+xml' in content_type:
#                     return extract_content(response.text)
#                 else:
#                     return {
#                         "raw_content": response.text[:100000],
#                         "content_type": content_type,
#                         "method": "requests_other"
#                     }
#         except requests.exceptions.Timeout:
#             logger.warning(f"Request timed out (attempt {current_retry+1}/{max_retries})")
#             # Check if we still have time for a retry
#             if check_global_timeout() < global_timeout:
#                 return try_requests_method(current_retry + 1)
#             else:
#                 raise TimeoutError(f"Global timeout exceeded after request timeout")
#         except Exception as e:
#             logger.warning(f"Standard request failed (attempt {current_retry+1}/{max_retries}): {str(e)}")
#             # Check if we still have time for a retry
#             if current_retry < max_retries - 1 and check_global_timeout() < global_timeout:
#                 # Wait before retry with exponential backoff (but respect global timeout)
#                 backoff_time = min(2 ** current_retry, global_timeout - (time.time() - start_time))
#                 if backoff_time > 0:
#                     time.sleep(backoff_time)
#                 return try_requests_method(current_retry + 1)
#             raise
    
#     # Similar modifications for cloudscraper and selenium methods
#     def try_cloudscraper_method(current_retry=0):
#         # Check global timeout before attempting
#         elapsed = check_global_timeout()
        
#         if current_retry >= max_retries:
#             logger.warning(f"Exceeded maximum retries ({max_retries}) for cloudscraper method")
#             return None
        
#         # Calculate remaining time for this request
#         remaining_time = min(timeout, global_timeout - elapsed)
#         if remaining_time <= 0:
#             raise TimeoutError("Global timeout exceeded during cloudscraper attempt")
            
#         try:
#             with st.spinner(f"Attempting cloudscraper (try {current_retry+1}/{max_retries}, {remaining_time:.1f}s remaining)..."):
#                 scraper = cloudscraper.create_scraper(delay=5, browser='chrome')
#                 response = scraper.get(url, timeout=remaining_time)
                
#                 # Check global timeout again before processing response
#                 check_global_timeout()
                
#                 content_type = response.headers.get('Content-Type', '').lower()
                
#                 if 'application/pdf' in content_type or is_pdf:
#                     return extract_pdf_content(response.content)
#                 else:
#                     return extract_content(response.text)
#         except Exception as e:
#             logger.warning(f"CloudScraper method failed (attempt {current_retry+1}/{max_retries}): {str(e)}")
#             # Check if we still have time for a retry
#             if current_retry < max_retries - 1 and check_global_timeout() < global_timeout:
#                 backoff_time = min(2 ** current_retry, global_timeout - (time.time() - start_time))
#                 if backoff_time > 0:
#                     time.sleep(backoff_time)
#                 return try_cloudscraper_method(current_retry + 1)
#             return None
    
#     def try_selenium_method(current_retry=0):
#         # Check global timeout before attempting
#         elapsed = check_global_timeout()
        
#         if current_retry >= max_retries:
#             logger.warning(f"Exceeded maximum retries ({max_retries}) for selenium method")
#             return None
        
#         # Calculate remaining time for this request
#         remaining_time = min(timeout, global_timeout - elapsed)
#         if remaining_time <= 0:
#             raise TimeoutError("Global timeout exceeded during selenium attempt")
            
#         try:
#             with st.spinner(f"Attempting selenium (try {current_retry+1}/{max_retries}, {remaining_time:.1f}s remaining)..."):
#                 options = Options()
#                 options.add_argument("--headless")
#                 options.add_argument("--no-sandbox")
#                 options.add_argument("--disable-dev-shm-usage")
#                 options.add_argument(f"user-agent={random.choice(user_agents)}")
#                 options.add_argument("--disable-gpu")
#                 options.add_argument("--window-size=1920,1080")
#                 options.add_argument("--disable-extensions")
#                 options.add_argument("--disable-images")  # Optional: disable images to load faster
                
#                 # Add page load timeout
#                 options.page_load_strategy = 'eager'  # Don't wait for all resources, just DOM
                
#                 driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#                 driver.set_page_load_timeout(min(remaining_time, timeout))
                
#                 try:
#                     driver.get(url)
                    
#                     # Check global timeout before waiting
#                     elapsed_after_get = check_global_timeout()
                    
#                     # Calculate how much time we can still wait
#                     actual_wait_time = min(wait_time, global_timeout - elapsed_after_get)
#                     if actual_wait_time > 0:
#                         time.sleep(actual_wait_time)
                    
#                     # Check global timeout again before getting page source
#                     check_global_timeout()
                    
#                     page_source = driver.page_source
#                     driver.quit()
                    
#                     return extract_content(page_source)
#                 except Exception as inner_e:
#                     logger.warning(f"Selenium page load failed: {str(inner_e)}")
#                     driver.quit()
#                     raise
                    
#         except Exception as e:
#             logger.warning(f"Selenium method failed (attempt {current_retry+1}/{max_retries}): {str(e)}")
#             # Check if we still have time for a retry
#             if current_retry < max_retries - 1 and check_global_timeout() < global_timeout:
#                 backoff_time = min(2 ** current_retry, global_timeout - (time.time() - start_time))
#                 if backoff_time > 0:
#                     time.sleep(backoff_time)
#                 return try_selenium_method(current_retry + 1)
#             return None
#     progress_bar = st.progress(0)
#     status_text = st.empty()
#     try:
#         methods_attempted = []
#         methods_succeeded = []
#         content = None
#         def update_progress():
#             elapsed = time.time() - start_time
#             progress = min(elapsed / global_timeout, 1.0)
#             progress_bar.progress(progress)
#             remaining = max(global_timeout - elapsed, 0)
#             status_text.text(f"Time remaining: {remaining:.1f}s / {global_timeout}s")
#             return elapsed
#         update_progress()
#         import threading
#         stop_progress_thread = threading.Event()
        
#         def progress_updater():
#             while not stop_progress_thread.is_set():
#                 update_progress()
#                 time.sleep(0.5)
                
#         progress_thread = threading.Thread(target=progress_updater)
#         progress_thread.daemon = True
#         progress_thread.start()
        
#         try:
#             try:
#                 methods_attempted.append("requests")
#                 content = try_requests_method()
#                 if content:
#                     methods_succeeded.append("requests")
#             except Exception as e:
#                 logger.info(f"Standard requests method failed: {str(e)}")
#                 if time.time() - start_time < global_timeout:
#                     if not is_pdf:
#                         methods_attempted.append("cloudscraper")
#                         content = try_cloudscraper_method()
#                         if content:
#                             methods_succeeded.append("cloudscraper")

#                     if not content and javascript and time.time() - start_time < global_timeout:
#                         methods_attempted.append("selenium")
#                         content = try_selenium_method()
#                         if content:
#                             methods_succeeded.append("selenium")
#         finally:
#             stop_progress_thread.set()
#             progress_thread.join(timeout=1.0)
#             elapsed = update_progress()
#             if elapsed >= global_timeout:
#                 status_text.warning(f"Global timeout reached ({global_timeout}s)")
#             else:
#                 status_text.success(f"Completed in {elapsed:.1f}s (limit: {global_timeout}s)")
#         if not content:
#             st.error("Failed to scrape the website with all available methods.")
#             return {
#                 "error": "Failed to scrape with all methods or timeout reached",
#                 "url": url,
#                 "methods_attempted": methods_attempted,
#                 "elapsed_time": time.time() - start_time,
#                 "global_timeout": global_timeout,
#                 "timestamp": time.time()
#             }
#         content["url"] = url
#         content["timestamp"] = time.time()
#         content["scrape_duration"] = time.time() - start_time
#         content["methods_attempted"] = methods_attempted
#         content["methods_succeeded"] = methods_succeeded

#         _scrape_cache[url] = content
#         st.success(f"Successfully scraped {url}")
        
#         return content
        
#     except TimeoutError as e:
#         print(f"Scraping timed out after {time.time() - start_time:.1f}s: {str(e)}")
#         return {
#             "error": str(e),
#             "url": url,
#             "elapsed_time": time.time() - start_time,
#             "global_timeout": global_timeout,
#             "methods_attempted": methods_attempted,
#             "timestamp": time.time()
#         }
#     except Exception as e:
#         print(f"Error scraping {url}: {str(e)}")
#         return {
#             "error": str(e),
#             "url": url,
#             "elapsed_time": time.time() - start_time,
#             "global_timeout": global_timeout,
#             "methods_attempted": methods_attempted,
#             "timestamp": time.time()
#         }
#     finally:
#         progress_bar.empty()
#         status_text.empty()







websocket_logger = logging.getLogger('tornado.websocket')
websocket_logger.setLevel(logging.ERROR)
asyncio_logger = logging.getLogger('asyncio')
asyncio_logger.setLevel(logging.CRITICAL)

_scrape_cache = {}

def scrape_website(url, javascript=False, wait_time=3):
    global _scrape_cache
    if url in _scrape_cache:
        st.info(f"Using cached scrape results for: {url}")
        return _scrape_cache[url]
    
    st.write(f"Scraping content from: {url}")
    
    is_pdf = url.lower().endswith('.pdf')
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    
    def get_domain(url):
        parsed_uri = urlparse(url)
        return '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    
    def clean_text(text):
        """Clean up extracted text"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        text = '\n'.join(line for line in text.splitlines() if line.strip())
        return text
    
    def extract_content(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        

        result = {
            "title": "",
            "all_text": "",
            "main_content": "",
            "links": [],
            "structured_data": {},
            "metadata": {},
            "html": html_content  
        }
        
        if soup.title:
            result["title"] = soup.title.get_text(strip=True)
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            result["metadata"]["description"] = meta_desc.get('content')

        for element in soup.select('script, style'):
            element.decompose()
        

        result["all_text"] = clean_text(soup.get_text(separator='\n', strip=True))
        
        main_content_selectors = ['main', '#content', '.content', 'article', '.article', '.post', '#main', '.main-content']
        for selector in main_content_selectors:
            content_elements = soup.select(selector)
            if content_elements:
                content = '\n'.join(element.get_text(separator='\n', strip=True) for element in content_elements)
                if len(content) > 200: 
                    result["main_content"] = clean_text(content)
                    break
        
        if not result["main_content"]:
            result["main_content"] = result["all_text"]
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            text = link.get_text(strip=True)
            if href and not href.startswith('#') and not href.startswith('javascript:'):
                result["links"].append({
                    "url": href,
                    "text": text
                })
        
        jsonld_elements = soup.select('script[type="application/ld+json"]')
        if jsonld_elements:
            structured_json = []
            for jsonld in jsonld_elements:
                try:
                    if jsonld.string:
                        json_data = json.loads(jsonld.string)
                        structured_json.append(json_data)
                except Exception as e:
                    logger.warning(f"Error parsing JSON-LD: {str(e)}")
            
            if structured_json:
                result["structured_data"]["json_ld"] = structured_json
        
        return result
    
    def extract_pdf_content(pdf_bytes):
        try:
            try:
                pdf_io = BytesIO(pdf_bytes)
                reader = PyPDF2.PdfReader(pdf_io)
                text_content = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text_content += page.extract_text() + "\n\n"
                result = {
                    "title": "PDF Document",
                    "all_text": text_content,
                    "main_content": text_content,
                    "links": [],
                    "structured_data": {},
                    "metadata": {
                        "pdf_pages": len(reader.pages),
                        "content_type": "application/pdf"
                    },
                    "is_pdf": True,
                    "pdf_extraction_method": "PyPDF2"
                }
                try:
                    info = reader.metadata
                    if info:
                        if hasattr(info, 'title') and info.title:
                            result["title"] = info.title
                        if hasattr(info, 'author'):
                            result["metadata"]["author"] = info.author
                        if hasattr(info, 'creator'):
                            result["metadata"]["creator"] = info.creator
                        if hasattr(info, 'producer'):
                            result["metadata"]["producer"] = info.producer
                        if hasattr(info, 'subject'):
                            result["metadata"]["subject"] = info.subject
                except Exception as e:
                    logger.warning(f"Error extracting PDF metadata: {str(e)}")
                
                return result
                
            except (ImportError, Exception) as e:
                logger.warning(f"PyPDF2 failed: {str(e)}, trying pdfplumber")
                
                
                pdf_io = io.BytesIO(pdf_bytes)
                with pdfplumber.open(pdf_io) as pdf:
                    text_content = ""
                    for page in pdf.pages:
                        text_content += page.extract_text() + "\n\n"
                    
                    result = {
                        "title": "PDF Document",
                        "all_text": text_content,
                        "main_content": text_content,
                        "links": [],
                        "structured_data": {},
                        "metadata": {
                            "pdf_pages": len(pdf.pages),
                            "content_type": "application/pdf"
                        },
                        "is_pdf": True,
                        "pdf_extraction_method": "pdfplumber"
                    }
                    
                    return result
        except ImportError:
            return {
                "title": "PDF Document",
                "all_text": "PDF content could not be extracted. PDF extraction libraries are required.",
                "main_content": "PDF content could not be extracted. Please install PyPDF2 or pdfplumber.",
                "links": [],
                "structured_data": {},
                "metadata": {
                    "content_type": "application/pdf",
                    "error": "PDF libraries not available"
                },
                "is_pdf": True,
                "pdf_extraction_method": "none"
            }
        except Exception as e:
            return {
                "title": "PDF Document",
                "all_text": f"Error extracting PDF content: {str(e)}",
                "main_content": f"Error extracting PDF content: {str(e)}",
                "links": [],
                "structured_data": {},
                "metadata": {
                    "content_type": "application/pdf",
                    "error": str(e)
                },
                "is_pdf": True,
                "pdf_extraction_method": "failed"
            }
    def try_requests_method():
        try:
            current_headers = headers.copy()
            current_headers['Referer'] = get_domain(url)
            
            session = requests.Session()
            response = session.get(
                url, 
                headers=current_headers, 
                timeout=20,
                allow_redirects=True
            )
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '').lower()
            
            if 'application/pdf' in content_type or is_pdf:
                return extract_pdf_content(response.content)
            elif 'application/json' in content_type:
                return {"json_data": response.json(), "method": "requests_json"}
            elif 'text/html' in content_type or 'application/xhtml+xml' in content_type:
                return extract_content(response.text)
            else:
                return {
                    "raw_content": response.text[:100000],
                    "content_type": content_type,
                    "method": "requests_other"
                }
        except Exception as e:
            logger.warning(f"Standard request failed: {str(e)}")
            raise
    
    def try_cloudscraper_method():
        try:
            scraper = cloudscraper.create_scraper(delay=5, browser='chrome')
            response = scraper.get(url)
            content_type = response.headers.get('Content-Type', '').lower()
            
            if 'application/pdf' in content_type or is_pdf:
                return extract_pdf_content(response.content)
            else:
                return extract_content(response.text)
        except Exception as e:
            logger.warning(f"CloudScraper method failed: {str(e)}")
            return None
    
    def try_selenium_method():
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"user-agent={random.choice(user_agents)}")
            
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)
            if wait_time > 0:
                time.sleep(wait_time)
            page_source = driver.page_source
            driver.quit()
            
            return extract_content(page_source)
        except Exception as e:
            logger.warning(f"Selenium method failed: {str(e)}")
            return None
    try:
        started_at = time.time()
        methods_attempted = []
        methods_succeeded = []
        content = None
        
        try:
            methods_attempted.append("requests")
            content = try_requests_method()
            if content:
                methods_succeeded.append("requests")
                st.write("Successfully scraped using standard requests")
        except Exception as e:
            logger.info(f"Standard requests method failed: {str(e)}")
            
            if not is_pdf:  
                methods_attempted.append("cloudscraper")
                content = try_cloudscraper_method()
                if content:
                    methods_succeeded.append("cloudscraper")
                    st.write("Successfully scraped using CloudScraper")

                if not content and javascript:
                    methods_attempted.append("selenium")
                    content = try_selenium_method()
                    if content:
                        methods_succeeded.append("selenium")
                        st.write("Successfully scraped using Selenium")
        if not content:
            st.error("Failed to scrape the website with all available methods.")
            return {
                "error": "Failed to scrape with all methods",
                "url": url,
                "methods_attempted": methods_attempted,
                "timestamp": time.time()
            }
        
        content["url"] = url
        content["timestamp"] = time.time()
        content["scrape_duration"] = time.time() - started_at
        content["methods_attempted"] = methods_attempted
        content["methods_succeeded"] = methods_succeeded
        if is_pdf or content.get("is_pdf", False) or content.get("metadata", {}).get("content_type") == "application/pdf":
            content["streamlit_display"] = {
                "content_type": "PDF Document",
                "title": content.get("title", "PDF Document"),
                "pages": content.get("metadata", {}).get("pdf_pages", "Unknown"),
                "text_preview": content.get("main_content", "")[:500] + "..." if content.get("main_content") else "No text content extracted",
                "extraction_method": content.get("pdf_extraction_method", "unknown")
            }
        
        _scrape_cache[url] = content
        st.success(f"Successfully scraped {url}")
        
        return content
        
    except Exception as e:
        st.error(f"Error scraping {url}: {str(e)}")
        return {
            "error": str(e),
            "url": url,
            "timestamp": time.time()
        }
