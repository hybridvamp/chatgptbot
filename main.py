import os
from telethon import TelegramClient, events
from chatgpt.models.chatgpt import ChatGPT

bot_token = os.environ['BOT_TOKEN']

client = TelegramClient(bot_token, api_id=None, api_hash=None)
client.start(bot_token=bot_token)

chatbot = ChatGPT()
chatbot.load_model()

@client.on(events.NewMessage)
async def handle_message(event):
    user_message = event.raw_text
    response = chatbot.get_response(user_message)
    await event.respond(response)

client.run_until_disconnected()
