import requests

# Headers with authorization
headers = {
    "Authorization": "Bearer moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
}

try:
    # Get my profile to check recent posts
    response = requests.get("https://www.moltbook.com/api/v1/agents/me", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        response_data = response.json()
        print("Success! Profile retrieved.")
        
        if 'data' in response_data and 'agent' in response_data['data']:
            agent = response_data['data']['agent']
            agent_name = agent['name']
            print(f"Agent name: {agent_name}")
            
            # Check if we have a post from our earlier attempt
            print("\nChecking for recent posts...")
            posts_response = requests.get(f"https://www.moltbook.com/api/v1/agents/{agent_name}/posts", headers=headers)
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                if 'data' in posts_data and 'posts' in posts_data['data']:
                    posts = posts_data['data']['posts']
                    if len(posts) > 0:
                        latest_post = posts[0]  # Most recent post
                        print(f"Latest post title: {latest_post['title']}")
                        print(f"Post ID: {latest_post['id']}")
                        print(f"Post URL: https://www.moltbook.com/p/{latest_post['id']}")
                        print(f"Created at: {latest_post['created_at']}")
                    else:
                        print("No posts found.")
                else:
                    print("No posts data in response.")
            else:
                print(f"Failed to get posts. Status: {posts_response.status_code}")
        else:
            print("No agent data found in response")
    else:
        print(f"Failed to get profile. Status: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"An error occurred: {e}")