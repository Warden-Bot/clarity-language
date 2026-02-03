#!/usr/bin/env python3
"""
Check Moltbook status to verify API key works
"""

import urllib.request
import json

def check_status():
    # API configuration
    api_key = "moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
    url = "https://www.moltbook.com/api/v1/agents/status"
    
    # Create the request
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {api_key}'
    })
    
    try:
        # Make the request
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        
        print("Moltbook status check successful!")
        print(f"Status: {json.dumps(result, ensure_ascii=True)}")
        return result
    except urllib.error.HTTPError as e:
        print(f"Failed to check status. HTTP Error: {e.code}")
        error_response = e.read().decode('utf-8', errors='ignore')
        print(f"Response: {error_response}")
        return None
    except Exception as e:
        print(f"Failed to check status. Error: {str(e)}")
        return None

if __name__ == "__main__":
    check_status()