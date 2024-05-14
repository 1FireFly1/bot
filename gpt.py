import requests
from config import headers, FOLDER_ID, TEMPERATURE, MAX_TOKENS, URL



def promt_gpt(text):

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": TEMPERATURE,
            "maxTokens": MAX_TOKENS
        },
        "messages": [
            {
                "role": "user",
                "text": text
            }
        ]
    }

    try:
        response = requests.post(URL,
                                 headers=headers,
                                 json=data)

        if response.status_code == 200:
            text = response.json()["result"]["alternatives"][0]["message"]["text"]

    except Exception as x:
        text = "Something went wrong!"

    return text