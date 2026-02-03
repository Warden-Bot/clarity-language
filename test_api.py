import requests
import json

# Test if our API key works by trying to get our agent info
headers = {
    "Authorization": "Bearer moltbook_sk_UYrHXtPzmKYSfKu-nfKKSpFK9M-qEB50",
    "Content-Type": "application/json"
}

print("Testing API key with agent info request...")
try:
    response = requests.get("https://www.moltbook.com/api/v1/agents/me", headers=headers)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("API key is valid! Got successful response.")
        data = response.json()
        if 'data' in data and 'agent' in data['data']:
            agent_name = data['data']['agent']['name']
            print(f"Agent name: {agent_name}")
        else:
            print("Got successful response but unexpected data structure")
    elif response.status_code == 401:
        print("API key is invalid or unauthorized")
    elif response.status_code == 500:
        print("Server error - API might be temporarily down")
    else:
        print(f"Unexpected status code: {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"Request failed with error: {e}")

print("\nTrying to access public posts (without auth)...")
try:
    # Try to get public posts without auth to see if API is working
    pub_response = requests.get("https://www.moltbook.com/api/v1/posts?limit=2")
    print(f"Public posts status: {pub_response.status_code}")
    if pub_response.status_code == 200:
        print("Public API is accessible")
    else:
        print(f"Public API returned status: {pub_response.status_code}")
except Exception as e:
    print(f"Public API request failed: {e}")