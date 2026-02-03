import requests
import json

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
        
        # Write response to file to avoid encoding issues
        with open("comments_debug.json", "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=2, ensure_ascii=False)
        
        # Check the actual structure based on the keys we saw
        if 'comments' in response_data:
            comments = response_data['comments']
            print(f"Found {len(comments)} comments:")
            
            for i, comment in enumerate(comments):
                author = comment.get('author', {}).get('name', 'Unknown')
                content = comment.get('content', 'No content')
                comment_id = comment.get('id', 'Unknown ID')
                
                print(f"\n{i+1}. Author: {author}")
                print(f"   ID: {comment_id}")
                
                # Write content to file to avoid encoding issues
                print(f"   Content saved to file (due to encoding)")
                
                # Save the comment content to a separate file
                with open(f"comment_{i+1}_from_{author}.txt", "w", encoding="utf-8") as f:
                    f.write(f"Author: {author}\n")
                    f.write(f"ID: {comment_id}\n")
                    f.write(f"Content:\n{content}\n")
                
                # Check if this is from ZhihuThinker2
                if 'zhihu' in author.lower() or 'thinker' in author.lower():
                    print("   >>> This is the ZhihuThinker2 comment we're looking for!")
                    
                    # Save as a special file for reference
                    with open("zhihu_comment.txt", "w", encoding="utf-8") as f:
                        f.write(f"ZhihuThinker2 Comment:\n{content}\n")
                        
        else:
            print("No comments found in response")
            print("Available keys:", response_data.keys())
    else:
        print(f"Failed to get comments. Status: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()