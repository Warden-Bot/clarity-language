#!/usr/bin/env python3
"""
Search Moltbook for relevant subs or posts
"""

import urllib.request
import json

def search_moltbook(query):
    # API configuration (using the same key for authentication if needed)
    api_key = "moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
    
    # Different search endpoints to try
    search_urls = [
        f"https://www.moltbook.com/api/v1/search?q={query}",
        f"https://www.moltbook.com/api/v1/posts/search?q={query}",
        f"https://www.moltbook.com/api/v1/submolts/search?q={query}",
        f"https://www.moltbook.com/api/v1/explore?q={query}"
    ]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    for url in search_urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            
            # Make the request
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode('utf-8'))
            
            print(f"Search results from {url}:")
            print(json.dumps(result, indent=2))
            return result
        except urllib.error.HTTPError as e:
            print(f"Search failed on {url}. HTTP Error: {e.code}")
            print(f"Response: {e.read().decode('utf-8')}")
            continue
        except Exception as e:
            print(f"Search failed on {url}. Error: {str(e)}")
            continue
    
    print("All search attempts failed")
    return None

def get_trending_posts():
    """Get trending posts on Moltbook"""
    api_key = "moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
    
    urls = [
        "https://www.moltbook.com/api/v1/posts/trending",
        "https://www.moltbook.com/api/v1/posts/popular",
        "https://www.moltbook.com/api/v1/explore",
        "https://www.moltbook.com/api/v1/posts/recent"
    ]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode('utf-8'))
            
            print(f"Trending posts from {url}:")
            print(json.dumps(result, indent=2))
            return result
        except Exception as e:
            print(f"Trending posts request failed on {url}. Error: {str(e)}")
            continue
    
    print("All trending posts attempts failed")
    return None

def get_submolts():
    """Get available submolts on Moltbook"""
    api_key = "moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
    
    urls = [
        "https://www.moltbook.com/api/v1/submolts",
        "https://www.moltbook.com/api/v1/submolts/popular",
        "https://www.moltbook.com/api/v1/explore/submolts"
    ]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode('utf-8'))
            
            print(f"Submolts from {url}:")
            print(json.dumps(result, indent=2))
            return result
        except Exception as e:
            print(f"Submolts request failed on {url}. Error: {str(e)}")
            continue
    
    print("All submolts attempts failed")
    return None

if __name__ == "__main__":
    print("=== SEARCHING FOR PROGRAMMING LANGUAGE TOPICS ===")
    search_moltbook("programming language")
    
    print("\n=== SEARCHING FOR AI AGENT TOPICS ===")
    search_moltbook("AI agent")
    
    print("\n=== SEARCHING FOR COLLABORATION TOPICS ===")
    search_moltbook("collaboration")
    
    print("\n=== GETTING TRENDING POSTS ===")
    get_trending_posts()
    
    print("\n=== GETTING AVAILABLE SUBMOLTS ===")
    get_submolts()