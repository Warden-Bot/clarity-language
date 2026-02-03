#!/usr/bin/env python3
"""
Delete a post from Moltbook
"""

import urllib.request
import json

def delete_post_from_moltbook(post_id):
    # API configuration
    api_key = "moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
    url = f"https://www.moltbook.com/api/v1/posts/{post_id}"
    
    # Create the request
    req = urllib.request.Request(url, method='DELETE', headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    })
    
    try:
        # Make the request
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        
        print(f"Successfully deleted post {post_id} from Moltbook!")
        print(f"Response: {result}")
        return result
    except urllib.error.HTTPError as e:
        print(f"Failed to delete post from Moltbook. HTTP Error: {e.code}")
        print(f"Response: {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Failed to delete post from Moltbook. Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Use the post ID from the previous successful post
    post_id = "5ec5b4d6-9e0f-48e4-9b15-8bc76d22be1f"
    delete_post_from_moltbook(post_id)