import re
import json
import urllib3

http = urllib3.PoolManager()

url = 'http://ipinfo.io/json'
response = http.request('GET', url)
data = json.load(response)
print(data)