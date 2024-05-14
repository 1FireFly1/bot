import requests
from config import IAM_TOKEN, FOLDER_ID, URL_TOKENIZE, headers
import json


token = IAM_TOKEN

folder_id = FOLDER_ID


def count_tokens(text):
    data = {
        "modelUri": f"gpt://{folder_id}/yandexgpt-lite/latest",
        "text": text
    }
    return len(
        requests.post(
            URL_TOKENIZE,
            json=data,
            headers=headers
        ).json()['tokens']
    )
