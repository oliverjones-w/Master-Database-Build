import requests
import os

# API endpoint URL
api_url = "https://api.openai.com/v1/chat/completions"

# API key (replace with your actual key)
api_key = os.environ.get("GPT3_API_KEY")

# Check if the environment variable exists and has a value
if api_key is not None:
    # Use the api_key in your code
    print(f"API Key: {api_key}")
else:
    print("Environment variable not found or has no value.")


# Request headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Request data
data = {
    "model": "gpt-3.5-turbo-1106",
    "messages":  [{"role": "system", "content": "You are a database query assistant."},
        {"role": "assistant", "content": "The database schema is as follows:"},
        {"role": "assistant", "content": "File: C:\\Users\\BSA-OliverJ'22\\Projects\\Database Architecture\\SQLFiles\\MasterDatabaseFullScript.sql"},
        {"role": "user", "content": "Generate a SQL query for the profiles that don't have mobile numbers."}]
}


# Make the API request
response = requests.post(api_url, headers=headers, json=data)

# Parse and print the response
if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"API request failed with status code {response.status_code}: {response.text}")