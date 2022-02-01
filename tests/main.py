import requests

# dummy test
print("start")
r = requests.get('http://127.0.0.1')
if r.status_code != 200:
    print("1")
    exit(1)
print("0")
exit(0)
