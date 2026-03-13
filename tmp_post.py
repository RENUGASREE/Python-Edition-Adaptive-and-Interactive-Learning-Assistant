import json
import urllib.request
import urllib.error

url = 'https://python-edition-adaptive-and-interactive.onrender.com/api/auth/register'
payload = {
    'username': 'rendertestuser',
    'email': 'rendertestuser@example.com',
    'password': 'Test1234',
    'full_name': 'Render Test',
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    resp = urllib.request.urlopen(req, timeout=30)
    print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('HTTP', e.code, e.read().decode())
except Exception as e:
    print('ERROR', e)
