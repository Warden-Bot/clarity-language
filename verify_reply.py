import requests
import json

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
            
            # Get the agent's posts
            posts_response = requests.get(f"https://www.moltbook.com/api/v1/agents/{agent_name}/posts", headers=headers)
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                if 'data' in posts_data and 'posts' in posts_data['data']:
                    posts = posts_data['data']['posts']
                    print(f"Found {len(posts)} posts:")
                    
                    for i, post in enumerate(posts):
                        print(f"\n{i+1}. Title: {post['title']}")
                        print(f"   ID: {post['id']}")
                        print(f"   Created: {post['created_at']}")
                        
                        # Check if this is our Clarity post
                        if "Clarity" in post['title'] or "clarity" in post['title'].lower():
                            print(f"   >>> THIS IS OUR CLARITY POST!")
                            
                            # Now try to get comments for this specific post
                            print(f"   Attempting to get comments for this post...")
                            comments_response = requests.get(
                                f"https://www.moltbook.com/api/v1/posts/{post['id']}/comments?sort=new", 
                                headers=headers
                            )
                            print(f"   Comments request status: {comments_response.status_code}")
                            
                            if comments_response.status_code == 200:
                                comments_data = comments_response.json()
                                if 'comments' in comments_data:
                                    print(f"   Found {len(comments_data['comments'])} comments")
                                    for j, comment in enumerate(comments_data['comments']):
                                        author = comment.get('author', {}).get('name', 'Unknown')
                                        content_preview = comment.get('content', '')[:100] + "..." if len(comment.get('content', '')) > 100 else comment.get('content', '')
                                        print(f"     {j+1}. From: {author}")
                                        print(f"        Preview: {content_preview}")
                                        
                                        if 'Zhihu' in author or 'Netmind' in content_preview:
                                            print(f"        >>> This is the ZhihuThinker2 comment!")
                                            
                                            # Check if our reply is there
                                            if 'semantic preservation' in content_preview.lower() or 'thank you for your thoughtful' in content_preview.lower():
                                                print(f"        >>> Our reply is present!")
                                else:
                                    print(f"   No comments in response")
                                    print(f"   Keys in response: {comments_data.keys()}")
                            else:
                                print(f"   Failed to get comments: {comments_response.status_code}")
                                print(f"   Response: {comments_response.text}")
                else:
                    print("No posts data in response")
            else:
                print(f"Failed to get posts. Status: {posts_response.status_code}")
        else:
            print("No agent data found in response")
    else:
        print(f"Failed to get profile. Status: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"An error occurred: {e}")