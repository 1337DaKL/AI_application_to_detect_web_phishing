import requests

url = "http://127.0.0.1:5000/predict"
data = {"url": "https://allegrolokalne.pl-1111.cyou"}

response = requests.post(url, json=data)
print(response.json())
