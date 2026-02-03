#!/usr/bin/env python3
"""
Search Moltbook for specific programming and AI related topics
"""

import urllib.request
import json
from urllib.parse import quote

def search_moltbook_encoded(query):
    """Search using URL encoding for spaces"""
    # API configuration
    api_key = "moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
    
    # Encode the query parameter properly
    encoded_query = quote(query)
    url = f"https://www.moltbook.com/api/v1/submolts/search?q={encoded_query}"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        
        # Make the request
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        
        print(f"Search results for '{query}':")
        print(json.dumps(result, indent=2))
        return result
    except urllib.error.HTTPError as e:
        print(f"Search failed for '{query}'. HTTP Error: {e.code}")
        print(f"Response: {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Search failed for '{query}'. Error: {str(e)}")
        return None

def search_for_programming_topics():
    """Search for programming-related topics"""
    topics = [
        "programming",
        "code",
        "software",
        "development",
        "language",
        "AI",
        "artificial intelligence",
        "agent",
        "collaboration",
        "open source",
        "github"
    ]
    
    results = {}
    for topic in topics:
        print(f"\n--- Searching for: {topic} ---")
        result = search_moltbook_encoded(topic)
        results[topic] = result
    
    return results

def browse_popular_submolts():
    """Browse popular submolts that might be relevant"""
    api_key = "moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
    
    # Try different endpoints to get popular/relevant submolts
    urls = [
        "https://www.moltbook.com/api/v1/submolts?sort=subscriber_count&limit=20",
        "https://www.moltbook.com/api/v1/submolts?sort=activity&limit=20",
        "https://www.moltbook.com/api/v1/explore/submolts"
    ]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    for url in urls:
        try:
            print(f"\n--- Browsing submolts from: {url} ---")
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode('utf-8'))
            
            print(json.dumps(result, indent=2))
            return result
        except Exception as e:
            print(f"Browsing submolts failed on {url}. Error: {str(e)}")
            continue
    
    return None

if __name__ == "__main__":
    print("=== SEARCHING FOR PROGRAMMING & AI RELATED TOPICS ===")
    search_results = search_for_programming_topics()
    
    print("\n=== BROWSING POPULAR SUBMOLTS ===")
    browse_popular_submolts()