import requests

#response = requests.get("https://projeslatic.internal:9200")
response = requests.get("https://projeslatic.fly.dev/")
print(response.json())
