"""import subprocess
import json

# Define the API key and the command
api_key = "ebd5e08a-0a6f-4f8f-9801-95001c33da6b"  # Replace YOUR_API_KEY with your actual API key

# Define the payload as a JSON string
payload = json.dumps({
    "stream": True,
    "model": "Meta-Llama-3.1-8B-Instruct",
    "messages": [
        {
            "role": "system",
            "content": "who is the richest person in the world?"
        },
    ]
})

# Construct the curl command
curl_command = [
    "curl",
    "-H", f"Authorization: Bearer {api_key}",
    "-H", "Content-Type: application/json",
    "-d", payload,
    "-X", "POST", "https://api.sambanova.ai/v1/chat/completions"
]

# Execute the curl command using subprocess
result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check if the command was successful
if result.returncode == 0:
    print("Response from API:")
    print(result.stdout)
else:
    print(f"Error occurred: {result.stderr}")
"""
import os
import openai

def api(prompt):
    os.environ['SAMBANOVA_API_KY'] = 'd17279e2-2af0-4dd0-850e-f02cf1b06f6e'
    client = openai.OpenAI(
        api_key=os.environ.get("SAMBANOVA_API_KY"),
        base_url="https://api.sambanova.ai/v1",
    )

    response = client.chat.completions.create(
        model='Meta-Llama-3.1-8B-Instruct',
        messages=prompt,
        temperature=0.1,
        top_p=0.1
    )

    return response.choices[0].message.content
