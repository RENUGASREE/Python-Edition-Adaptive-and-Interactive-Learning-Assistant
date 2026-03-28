import urllib.request
import json
import urllib.error

data = json.dumps({
    'email': 'noslash123@test.com',
    'password': 'StrongPassword123!'
}).encode('utf-8')

# Note the MISSING trailing slash here, like what the frontend does.
req = urllib.request.Request('http://localhost:8000/api/auth/register', data=data, headers={'Content-Type': 'application/json'})

try:
    res = urllib.request.urlopen(req)
    print("SUCCESS", res.code)
    print(res.read())
except urllib.error.HTTPError as e:
    print("FAILED", e.code)
    print(e.read().decode('utf-8'))
