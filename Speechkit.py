import requests
import math
from db import *
from config import BLOCKS, DURATION, USER_LIMIT, IAM_TOKEN, URL_SYNTHESIZE,URL_RECOGNIZE, FOLDER_ID, headers

token = IAM_TOKEN
folder_id = FOLDER_ID

def speech_to_text(voice):
    params = "&".join([
        "topic=general",
        f"folderId={folder_id}",
        "lang=ru-RU"
    ])

    response = requests.post(f"{URL_RECOGNIZE}{params}",
                             headers=headers,
                             data=voice
                             )

    decoded_data = response.json()
    if decoded_data.get("error_code") is None:
        print(decoded_data)
        return decoded_data.get("result")
    print(response.json())
    return "Error while requesting"

def text_to_speech(text):

    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'filipp',
        'folderId': folder_id,
    }
    response = requests.post(URL_SYNTHESIZE, headers=headers, data=data)
    if response.status_code == 200:
        result = response.content
        with open("file.ogg", 'wb') as f:
            f.write(result)
        return True, result
    else:
        result1 = "Error while requesting"
        return False, result1

def is_stt_block_limit(user_id, duration):
    audio_blocks = math.ceil(duration / BLOCKS)
    stt_user = SttBlocksInfo()
    result_stt = stt_user.stt_blocks_user(user_id)
    stt_user.close()
    if duration >= DURATION:
        return "The message is too long!"
    if result_stt >= USER_LIMIT:
        return f"Limit reached"
    all_blocks = result_stt + audio_blocks
    voice_control_add_user = SttBlocksAdd()
    voice_control_add_user.add_stt_blocks(all_blocks, user_id)
    voice_control_add_user.close()
def stt_symbols_db_to_text(user_id, text):
    info_db_tokens1 = TtsSymbolsInfo()
    tokens_db1 = info_db_tokens1.tts_symbols_user(user_id)
    result = tokens_db1 - len(text)
    info_db_tokens1.close()

    save_tokens = TtsSymbolsAdd()
    save_tokens.add_tts_symbols(result, user_id)
    save_tokens.close()

    text_db = MessageInfo()
    result_text = text_db.select_message(user_id)
    text_db.close()
    save_text = MessageAdd()
    if result_text is None:
        save_text.add_message(text, user_id)
    else:
        save_text.add_message(f'{result_text}\n\n' + text, user_id)
    save_text.close()
def stt_symbols_db(user_id, text):
    info_db_tokens1 = tokens_user()
    tokens_db1 = info_db_tokens1.tts_symbols_user(user_id)
    result = tokens_db1 + len(text)
    info_db_tokens1.close()

    save_tokens = tokens_add()
    save_tokens.add_tts_symbols(result, user_id)
    save_tokens.close()

    save_text = message_add()
    save_text.add_text(text, user_id)
    save_text.close()
def tk(text):
    ctrl = len(text)
    return ctrl