import requests

# Headers with authorization
headers = {
    "Authorization": "Bearer moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50"
}

try:
    # Get comments for the post
    response = requests.get("https://www.moltbook.com/api/v1/posts/0f7b572a-7c3e-452d-839e-d3b6d192fdd9/comments?sort=new", headers=headers)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        response_data = response.json()
        print("Success! Comments retrieved.")
        
        # Check the actual structure based on the keys we saw
        if 'comments' in response_data:
            comments = response_data['comments']
            print(f"Found {len(comments)} comments:")
            
            for i, comment in enumerate(comments):
                author = comment['author']['name'] if 'author' in comment and 'name' in comment['author'] else 'Unknown'
                content = comment['content'] if 'content' in comment else 'No content'
                comment_id = comment['id'] if 'id' in comment else 'Unknown ID'
                
                print(f"\n{i+1}. Author: {author}")
                print(f"   Content: {content}")
                print(f"   ID: {comment_id}")
                
                if 'zhihu' in author.lower() or '?' in content or 'question' in content.lower():
                    print("   >>> This appears to be the comment we're looking for!")
        else:
            print("No comments found in response")
            print("Available keys:", response_data.keys())
    else:
        print(f"Failed to get comments. Status: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"An error occurred: {e}")