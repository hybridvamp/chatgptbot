import openai
import os
import telethon
from telethon.sync import TelegramClient
import requests

api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
openai_api_key = os.environ.get("OPENAI_API_KEY")
telegraph_token = os.environ.get("TELEGRAPH_TOKEN")

client = TelegramClient(session='session_name', api_id=api_id, api_hash=api_hash)
client.start(bot_token=bot_token)

openai.api_key = openai_api_key

# /start command
@client.on(telethon.events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond("Hello! I am a Telegram bot powered by the OpenAI ChatGPT model.\nTo use me send your questions along with /ask command.\n\n(c) Made by @HYBRID_Bots")

# Handle all other messages
@client.on(telethon.events.NewMessage)
async def message_handler(event):
    if event.message.message.strip().startswith("/ask"):
        # Send message to notify user that response is being generated
        await event.reply("generating response...")

        # Get the message text
        message_text = event.message.message.strip().replace("/ask","",1).strip()

        # Pass event object to callback function
        openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{message_text}\n",
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
            callback=handle_response
        )


def handle_response(response):
    # Create a Telegraph article
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {telegraph_token}'
    }
    data = {
        'access_token': telegraph_token,
        'title': 'ChatGPT Response',
        'content': [{'tag': 'p', 'children': [{'text': response.choices[0].text}]}]
    }
    r = requests.post('https://api.telegra.ph/createPage', headers=headers, json=data)
    r_json = r.json()
    link = f"https://telegra.ph/{r_json['path']}"

    # Send the Telegraph link to the user
    event.respond(link)

# Run the bot
client.run_until_disconnected()