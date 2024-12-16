import requests
# Pip install requests by hand, wont be added to the requirements.txt file

function_url = "http://localhost:7071/api/drivers/{id}"

payload = {
    "driver": "3a14b8b0-bcbd-4dd5-90b4-de5fd5a13e78"
}

headers = {"Content-Type": "application/json"}

response = requests.put(function_url, json=payload, headers=headers)

print(f"HTTP Status Code: {response.status_code}")
print("Response Content:")
print(response.text)