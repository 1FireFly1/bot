import telebot
import logging
from db import *
from Speechkit import speech_to_text, text_to_speech, is_stt_block_limit, stt_symbols_db_to_text, tk, \
    stt_symbols_db
from Tokenizer import *
from gpt import *
from config import *




logging.basicConfig(
    filename=LOG_NAME,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="w",
)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start_handler(message):
    db_user = CreateDatabase()
    if not db_user.check_user_exists(message.chat.id):
        db_user.add_user(message.chat.id)
        bot.send_message(message.chat.id, "Hey! I'm a voice assistant bot. Ask me anything you want")
    else:
        bot.send_message(message.chat.id, "Welcome back!!!")

@bot.message_handler(commands=["tts"])
def send_tts(message):
    bot.send_message(message.chat.id, 'Text message:')

    def text_user1(message):
        text_message = message.text

        if message.content_type != 'text':
            bot.send_message(message.chat.id, 'Text message')

            bot.register_next_step_handler(message, text_user1)

            return

        if len(text_message) > 50:
            bot.send_message(message.chat.id, 'Message is way too long!')

            bot.register_next_step_handler(message, text_user1)

            return

        user_id = message.chat.id
        info_db_tokens = tokens_user()
        tokens_db = info_db_tokens.tts_symbols_user(user_id)
        info_db_tokens.close()
        if tokens_db != None and tokens_db > 0:
            save_text = message_add()
            save_text.add_text(text_message, user_id)
            save_text.close()
            info_tokens = tk(text_message)
            info_db_tokens1 = tokens_user()
            tokens_db1 = info_db_tokens1.tts_symbols_user(user_id)
            result = tokens_db1 - info_tokens
            info_db_tokens1.close()
            save_tokens = tokens_add()
            save_tokens.add_tts_symbols(result, user_id)
            save_tokens.close()
            success, response = text_to_speech(text_message)
            bot.send_message(message.chat.id, "Processing request")
            if success:
                bot.send_voice(message.chat.id, response)
            else:
                bot.send_message(message.chat.id, "Error:", response)
        else:
            bot.send_message(message.chat.id, 'Oops! You reached you symbols limit.')

    bot.register_next_step_handler(message, text_user1)


@bot.message_handler(commands=["stt"])
def voice_input(message):
    bot.send_message(message.chat.id, "Send me a voice message.")
    bot.register_next_step_handler(message, voice_gpt)


def voice_gpt(message):
    user_id = message.chat.id
    if not message.voice:
        return

    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file = bot.download_file(file_info.file_path)

    duration_user = message.voice.duration
    user_id = message.chat.id
    result_info = is_stt_block_limit(user_id=user_id, duration=duration_user)
    if result_info == 'Your message is way too long!' or result_info == 'Oops! Limit reached.':
        bot.send_message(message.chat.id, result_info)
        return

    voice_speechkit = speech_to_text(file)
    stt_symbols_db(user_id, voice_speechkit)
    bot.send_message(message.chat.id, f'<i>*{voice_speechkit}.*</i>', parse_mode='html')

@bot.message_handler(content_types=["voice"])
def voice_message_handler_message(message):
    voice = message.voice.file_id
    user_id = message.chat.id
    info_tokens = TotalGptTokensInfo()
    result_tokens = info_tokens.total_gpt_tokens_user(user_id)
    info_tts = TtsSymbolsInfo()
    result_tts = info_tts.tts_symbols_user(user_id)
    info_tts.close()
    info_tokens.close()
    if result_tokens is None or result_tokens < 0:
        result_tokens = 0
    if result_tts is None or result_tts < 0:
        result_tts = 0
    if int(result_tokens) > 0 and int(result_tts) > 0:
        file_info = bot.get_file(voice)
        file = bot.download_file(file_info.file_path)
        duration_user = message.voice.duration
        result_info = is_stt_block_limit(user_id=user_id, duration=duration_user)
        if result_info == 'Your message is way too long!' or result_info == 'Oops! Limit reached!':
            bot.send_message(message.chat.id, result_info)
            return
        voice_speechkit = speech_to_text(file)
        if voice_speechkit != 'Error while requesting':
            gpt_response = promt_gpt(voice_speechkit)
            if gpt_response != 'Error':
                tokenizer = count_tokens(voice_speechkit + gpt_response)
                save_tokens = TotalGptTokensAdd()
                save_tokens.add_total_gpt_tokens(result_tokens - tokenizer, user_id)
                save_tokens.close()
                status, result_text = text_to_speech(gpt_response)
                if result_text != 'Error while requesting':
                    stt_symbols_db_to_text(user_id, voice_speechkit)
                    stt_symbols_db_to_text(user_id, gpt_response)
                    bot.send_voice(message.chat.id, result_text)
                else:
                    bot.send_message(message.chat.id, "Error while requesting")
            else:
                bot.send_message(message.chat.id, "Error while requesting")
        else:
            bot.send_message(message.chat.id, "Error while requesting")

    else:
        bot.send_message(message.chat.id, "Request limit reached")

@bot.message_handler(commands=['debug'], func=lambda message: message.from_user.id == 5280322818) #сюда пихать свой юзер id телеграмма
def debug(message):
    with open('errors.cod.log', 'rb') as er:
        bot.send_document(message.chat.id, er)

@bot.message_handler(content_types=["text"])
def text_message_handler_message(message):
    text = message.text
    user_id = message.chat.id
    info_tokens = TotalGptTokensInfo()
    result_tokens = info_tokens.total_gpt_tokens_user(user_id)
    info_tokens.close()
    if result_tokens is None or result_tokens < 0:
        result_tokens = 0
    if int(result_tokens) > 0:
        gpt_response = promt_gpt(text)
        if gpt_response != 'Error':
            bot.send_message(message.chat.id, gpt_response)
            stt_symbols_db_to_text(user_id, text)
            stt_symbols_db_to_text(user_id, gpt_response)
            tokenizer = count_tokens(text + gpt_response)
            save_tokens = TotalGptTokensAdd()
            save_tokens.add_total_gpt_tokens(result_tokens - tokenizer, user_id)
            save_tokens.close()
        else:
            bot.send_message(message.chat.id, 'Error while requesting')
    else:
        bot.send_message(message.chat.id, 'Request limit reached!')

bot.infinity_polling()