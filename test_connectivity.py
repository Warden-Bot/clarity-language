import urllib.request
import urllib.error
import ssl

# Test basic connectivity to moltbook
try:
    # Create unverified context to bypass SSL issues if any
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(
        'https://www.moltbook.com/api/v1/agents/me',
        headers={
            'Authorization': 'Bearer moltbook_sk_knYhCgGXARBvlkJClI-1R1gtSn3zFdTo',
            'Content-Type': 'application/json'
        }
    )
    
    response = urllib.request.urlopen(req, context=ctx, timeout=10)
    print("Connection successful!")
    print(f"Status: {response.getcode()}")
    print(f"Response: {response.read().decode('utf-8')}")
    
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
    print(f"Response body: {e.read().decode('utf-8')}")
except urllib.error.URLError as e:
    print(f"URL Error: {e.reason}")
except Exception as e:
    print(f"General error: {e}")