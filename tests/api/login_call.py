import requests

# Define the URL of the API endpoint
url = "https://127.0.0.1:5000/api/account/register"

# Define the JSON data to be sent in the request body
data = {"username": "Blabla-123", "password": "Blabla-123", "email": "Email@email.com"}

# Make a POST request to the API endpoint with the JSON data
response = requests.post(url, json=data, verify=False)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the response content (JSON data)
    print(response.json())
else:
    # If the request was not successful, print the status code and error message
    print(f"Error: {response.status_code} - {response.text}")
