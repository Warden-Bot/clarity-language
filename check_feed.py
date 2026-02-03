import requests

# Headers with authorization
headers = {
    "Authorization": "Bearer moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
}

try:
    # Get the general feed to see if our post is there
    response = requests.get("https://www.moltbook.com/api/v1/posts?sort=new&limit=10", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        response_data = response.json()
        
        if 'data' in response_data and 'posts' in response_data['data']:
            posts = response_data['data']['posts']
            print(f"Found {len(posts)} recent posts:")
            
            for i, post in enumerate(posts):
                print(f"{i+1}. Title: {post['title'][:50]}{'...' if len(post['title']) > 50 else ''}")
                print(f"   Author: {post['author']['name']}")
                print(f"   ID: {post['id']}")
                print(f"   Created: {post['created_at']}")
                
                # Check if this is our Clarity post
                if "Clarity" in post['title'] or "clarity" in post['title'].lower():
                    print(f"   >>> THIS IS OUR POST! URL: https://www.moltbook.com/p/{post['id']}")
                
                print()
        else:
            print("No posts data in response")
    else:
        print(f"Failed to get feed. Status: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"An error occurred: {e}")