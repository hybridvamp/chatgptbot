import openai
import os
import telethon
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser

api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
openai_api_key = os.environ.get("OPENAI_API_KEY")

client = TelegramClient(api_id, api_hash, bot_token=bot_token).start()

openai.api_key = openai_api_key

# Handle the '/start' command
@client.on(telethon.events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond("Hello! I am a Telegram bot powered by the OpenAI ChatGPT model. How can I help you today?")

# Handle all other messages
@client.on(telethon.events.NewMessage)
async def message_handler(event):
    # Get the message text
    message_text = event.message.message.strip()

    # Use the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{message_text}\n",
        max_tokens=2048,
        n = 1,
        stop=None,
        temperature=0.5
    )

    # Send the response to the user
    await event.respond(response.choices[0].text)

# Run the bot
client.run_until_disconnected()