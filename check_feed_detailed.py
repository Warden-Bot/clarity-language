import requests

# Headers with authorization
headers = {
    "Authorization": "Bearer moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
}

try:
    # Try getting the feed instead
    response = requests.get("https://www.moltbook.com/api/v1/feed?sort=new&limit=10", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        response_data = response.json()
        print("Response:", response.text[:500])  # Print first 500 chars to see structure
        
        if 'data' in response_data and 'posts' in response_data['data']:
            posts = response_data['data']['posts']
            print(f"\nFound {len(posts)} posts in feed:")
            
            for i, post in enumerate(posts):
                print(f"{i+1}. Title: {post['title'][:50]}{'...' if len(post['title']) > 50 else ''}")
                print(f"   Author: {post['author']['name']}")
                print(f"   ID: {post['id']}")
                print(f"   Created: {post['created_at']}")
                
                # Check if this is our Clarity post
                if "Clarity" in post['title'] or "clarity" in post['title'].lower():
                    print(f"   >>> THIS IS OUR POST! URL: https://www.moltbook.com/p/{post['id']}")
                
                print()
        elif 'data' in response_data:
            print("Data object exists but no posts found in it")
            print("Available keys in data:", list(response_data['data'].keys()))
        else:
            print("No data object in response")
    else:
        print(f"Failed to get feed. Status: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"An error occurred: {e}")