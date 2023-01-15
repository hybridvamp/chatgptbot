import openai_secret_manager
import openai
import os
from telethon import TelegramClient, events

# Use your own API_ID and API_HASH from https://my.telegram.org
api_id = os.environ['API_ID']
api_hash = os.environ['API_HASH']

# Use the BOT_TOKEN you got from the BotFather
bot_token = os.environ['BOT_TOKEN']

# Create a new Telegram client using your API ID, Hash and Bot token
client = TelegramClient('session_name', api_id, api_hash, bot_token=bot_token).start()

def get_response(prompt):
    secrets = openai_secret_manager.get_secret("openai")
    openai_api_key = secrets["api_key"]
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        api_key=openai_api_key
    )
    return response.choices[0].text

# Define a callback function that will be called when the bot receives a message
@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    # Get the message text
    message_text = event.message.message

    # Check if the message is a command
    if message_text.startswith('/start'):
        # Send a greeting message to the user
        await event.respond("Hello! I am a language model trained by OpenAI. How can I help you today?")
    else:
        # Send a message to let the user know that the bot is generating a response
        await event.respond("generating response...")
        # Send the message text to me
        response_text = get_response(message_text)

        # Send the response text back to the user
        await event.respond(response_text)

# Start the bot
client.run_until_disconnected()