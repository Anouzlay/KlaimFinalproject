import re
import time
import random
from urllib.parse import urlparse
from typing import Dict, Any, List
from duckduckgo_search import DDGS
import streamlit as st

def enhanced_duckduckgo_search(query: str, all_queries: List[str], num_results: int = 2) -> Dict[str, Any]:
    # Initialize tracking variables
    results = []
    successful_queries = 0
    failed_queries = 0
    seen_domains = set()
    
    # Ensure UAE is explicitly included in the search
    if "UAE" not in query and "United Arab Emirates" not in query:
        query = f"UAE {query}"
    
    # Modify all queries to focus on UAE
    uae_queries = []
    for q in all_queries:
        if "UAE" not in q and "United Arab Emirates" not in q:
            uae_queries.append(f"UAE {q}")
        else:
            uae_queries.append(q)
    
    all_queries = uae_queries
    print(f"Beginning comprehensive search for UAE info: {query}")
    
    print(f"Beginning UAE-focused search for: {query}")
    progress_bar = st.progress(0)
    
    # Process all queries with improved exponential backoff for rate limiting
    for i, search_query in enumerate(all_queries):
        max_retries = 1  
        retry_count = 0
        backoff_time = 3  
        
        initial_delay = random.uniform(2, 5)
        time.sleep(initial_delay)
        
        # Try different backends if one fails
        backends = ["auto", "html", "lite"]
        backend_index = 0
        
        while retry_count < max_retries and backend_index < len(backends):
            current_backend = backends[backend_index]
            
            try:
                print(f"Searching for UAE info: {search_query} (using {current_backend} backend)")
                
                with DDGS(timeout=30) as ddgs:  # Increased timeout
                    # Configure the search with current backend
                    search_results = list(ddgs.text(
                        search_query, 
                        max_results=num_results,
                        backend=current_backend,
                        region="ae"  # Set region to UAE for more relevant results
                    ))
                
                # Process and filter results
                for result in search_results:
                    url = result.get("href", "")
                    domain = urlparse(url).netloc
                    
                    # Give priority to UAE domains
                    is_uae_domain = ".ae" in domain
                    
                    # Only add if we haven't seen too many from this domain
                    domain_count = sum(1 for r in results if urlparse(r.get("href", "")).netloc == domain)
                    if domain_count < 3:  # Limit to 3 results per domain for diversity
                        # Add source query to result for better tracking
                        result["source_query"] = search_query
                        result["backend_used"] = current_backend
                        results.append(result)
                
                successful_queries += 1
                
                # Add jittered delay between 3-8 seconds with randomness
                jitter = random.uniform(0.5, 1.5)
                delay = backoff_time * jitter
                print(f"Search successful for UAE info. Waiting {delay:.2f} seconds before next query")
                time.sleep(delay)
                break  # Exit retry loop on success
                
            except Exception as e:
                error_msg = str(e)
                print(f"Error on UAE query '{search_query}' using {current_backend}: {error_msg}")
                
                if "Ratelimit" in error_msg:
                    retry_count += 1
                    failed_queries += 1
                    
                    # More aggressive backoff with randomization
                    jitter = random.uniform(0.8, 1.2)
                    backoff_time = backoff_time * 2 * jitter  # Exponential backoff with jitter
                    
                    print(f"Rate limited. Waiting {backoff_time:.2f} seconds before retry {retry_count}/{max_retries}")
                    time.sleep(backoff_time)
                    
                    # Try a different backend if we've tried this one multiple times
                    if retry_count >= 2:
                        backend_index += 1
                        retry_count = 0  # Reset retry count for new backend
                        print(f"Switching to different backend: {backends[backend_index] if backend_index < len(backends) else 'none available'}")
                else:
                    # Handle other errors
                    retry_count += 1
                    failed_queries += 1
                    print(f"Search error. Waiting {backoff_time:.2f} seconds before retry {retry_count}/{max_retries}")
                    time.sleep(backoff_time)
                    
                    # If not a rate limit error but persistent, try another backend
                    if retry_count >= 2:
                        backend_index += 1
                        retry_count = 0
            
        # Update progress bar
        progress_bar.progress((i + 1) / len(all_queries))
        
        # Add a longer break between different search queries
        if i < len(all_queries) - 1:
            between_query_delay = random.uniform(5, 10)
            st.write(f"Moving to next UAE search query in {between_query_delay:.2f} seconds...")
            time.sleep(between_query_delay)
    
    # Extract unique URLs and add metadata
    processed_results = []
    seen_urls = set()
    
    # First pass: prioritize UAE domain results
    for r in results:
        url = r.get("href", "")
        domain = urlparse(url).netloc
        is_uae_domain = ".ae" in domain
        
        if is_uae_domain and url and url not in seen_urls:
            seen_urls.add(url)
            
            # Create enriched search result with UAE flag
            processed_results.append({
                "url": url,
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "source_query": r.get("source_query", ""),
                "backend_used": r.get("backend_used", ""),
                "domain": domain,
                "is_uae_domain": True,
                "likely_authority": "high"  # UAE domains get high authority
            })
    
    # Second pass: add other results
    for r in results:
        url = r.get("href", "")
        if url and url not in seen_urls:
            domain = urlparse(url).netloc
            seen_urls.add(url)
            url_lower = url.lower()
            
            # Create enriched search result
            processed_results.append({
                "url": url,
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "source_query": r.get("source_query", ""),
                "backend_used": r.get("backend_used", ""),
                "domain": domain,
                "is_uae_domain": False,
                "likely_authority": "high" if (
                    url_lower.startswith("https://www.") or 
                    ".gov" in url_lower or 
                    ".org" in url_lower or
                    "linkedin.com" in url_lower
                ) else "medium"
            })
    
    # Summary statistics
    st.success(f"Search complete! Found {len(processed_results)} unique UAE-related results")
    print(f"Successful queries: {successful_queries}/{len(all_queries)}")
    
    if failed_queries > 0:
        print(f"Failed queries: {failed_queries}")
    
    # Return categorized results for better processing
    categorized = {
        "results": processed_results,
        "statistics": {
            "total_unique_urls": len(processed_results),
            "successful_queries": successful_queries,
            "failed_queries": failed_queries,
            "uae_domains": sum(1 for r in processed_results if r.get("is_uae_domain", False)),
            "categories": {}
        }
    }
    
    return categorized