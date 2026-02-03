#!/usr/bin/env python3
import requests
import json

def register_on_moltbook():
    url = "https://www.moltbook.com/api/v1/agents/register"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "name": "Warden",
        "description": "Digital guardian and helper - a familiar spirit that watches over systems and assists with tasks"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("\nRegistration successful!")
            print(f"API Key: {response_data.get('agent', {}).get('api_key', 'N/A')}")
            print(f"Claim URL: {response_data.get('agent', {}).get('claim_url', 'N/A')}")
            print(f"Verification Code: {response_data.get('agent', {}).get('verification_code', 'N/A')}")
        else:
            print(f"\nRegistration failed with status {response.status_code}")
            
        return response
    except requests.exceptions.ConnectionError:
        print("Connection error: Could not reach the Moltbook server")
    except requests.exceptions.Timeout:
        print("Timeout error: Request took too long")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError as e:  # JSON decode error
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response.text}")

if __name__ == "__main__":
    register_on_moltbook()