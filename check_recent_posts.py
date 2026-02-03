import requests
import json

# Headers with authorization
headers = {
    "Authorization": "Bearer moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50",
    "Content-Type": "application/json"
}

try:
    # Get my profile to check recent posts
    response = requests.get("https://www.moltbook.com/api/v1/agents/me", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        response_data = response.json()
        print("Profile retrieved successfully!")
        
        if 'data' in response_data and 'agent' in response_data['data']:
            agent = response_data['data']['agent']
            agent_name = agent['name']
            print(f"Agent name: {agent_name}")
            
            # Now get the recent posts for this agent
            profile_response = requests.get(f"https://www.moltbook.com/api/v1/agents/profile?name={agent_name}", headers=headers)
            if profile_response.status_code == 200:
                profile_data = profile_response.json()
                if 'data' in profile_response.json() and 'recentPosts' in profile_response.json()['data']:
                    recent_posts = profile_response.json()['data']['recentPosts']
                    print(f"Found {len(recent_posts)} recent posts:")
                    for i, post in enumerate(recent_posts):
                        print(f"{i+1}. Title: {post['title']}")
                        print(f"   ID: {post['id']}")
                        print(f"   URL: https://www.moltbook.com/p/{post['id']}")
                        print(f"   Created: {post['created_at']}")
                        print()
                else:
                    print("No recent posts found in profile response")
            else:
                print(f"Failed to get profile. Status: {profile_response.status_code}")
                print(profile_response.text)
        else:
            print("No agent data found in response")
    else:
        print(f"Failed to get profile. Status: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"An error occurred: {e}")