import requests

# Call the API endpoint
response = requests.get("http://localhost:8000/", params={"user_id": 234})
print(response.status_code)
data = response.json()
print(data)
# Prints "Hello from the API!"