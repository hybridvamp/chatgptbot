import openai
import os
import telethon
from telethon.sync import TelegramClient
import json
import requests

api_keys = [os.environ.get("API_KEY1"), os.environ.get("API_KEY2"), os.environ.get("API_KEY3"), os.environ.get("API_KEY4"), os.environ.get("API_KEY5")]
current_api_key = 0

def switch_api_key():
    global current_api_key
    current_api_key = (current_api_key + 1) % len(api_keys)
    openai.api_key = api_keys[current_api_key]
    print(f'Switching to API key {current_api_key + 1}')

api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
telegraph_token = os.environ.get("TELEGRAPH_TOKEN")

client = TelegramClient(session='session_name', api_id=api_id, api_hash=api_hash)
client.start(bot_token=bot_token)

# /start command
@client.on(telethon.events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond("Hello! I am a Telegram bot powered by the OpenAI ChatGPT model.\nTo use me send your questions along with /ask command.\n\n(c) Made by @HYBRID_BOTS")

# Handle all other messages
@client.on(telethon.events.NewMessage)
async def message_handler(event):
    if event.message.message.strip().startswith("/ask"):
        # Send message to notify user that response is being generated
        generating_message = await event.reply("generating response...")
        
        # Get the message text
        message_text = event.message.message.strip().replace("/ask","",1).strip()

        # Pass event object to callback function
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"{message_text}\n",
                max_tokens=2048,
                n=1,
                stop=None,
                temperature=0.5,
            )
        except openai.exceptions.OpenAiError as e:
            if 'usage cap exceeded' in str(e):
                switch_api_key()
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"{message_text}\n",
                    max_tokens=2048,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
            else:
                raise e
        link = handle_response(event, response)
        await event.reply(link)
        await generating_message.delete()

def handle_response(event, response):
    # Create a Telegraph article
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {telegraph_token}'
    }
    data = {
        'access_token': telegraph_token,
        'title': 'ChatGPT Response',
        'content': [{'tag': 'p', 'children': [response.choices[0].text]}]
    }
    r = requests.post('https://api.telegra.ph/createPage', headers=headers, json=data)
    r_json = r.json()
    if r.status_code != 200 or not r_json['ok']:
        return "Error creating telegraph page"
    return f"https://telegra.ph/{r_json['result']['path']}"

# /stats command
@client.on(telethon.events.NewMessage(pattern='/stats'))
async def stats_handler(event):
    message = 'API key usage statistics: \n\n'
    for index, api_key in enumerate(api_keys):
        if not api_key:
            message += f'API key {index+1} : Not provided\n'
            continue
        usage = openai.Api.usage(api_key=api_key)
        message += f'API key {index+1} :\n'
        message += f'Queries today: {usage.queries_today} \n'
        message += f'Queries this month: {usage.queries_month} \n'
        message += f'Queries total: {usage.queries_total} \n'
    await event.respond(message)

# Run the bot
client.run_until_disconnected()