
import asyncio
from send_images import Bot

async def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    bot_token = '7193866015:AAHEHdNUyonQsM-5qLyjRxeBVZ7pA-QLziA'


    # Initialize the bot with your bot token
    bot = Bot(token=bot_token)

    # Replace 'YOUR_CHAT_ID' with the chat ID of your group
    chat_id = '4279700976'

    # The message you want to send to the group
    message = 'Hello from your bot!'

    # Send the message to the group
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == "__main__":
    asyncio.run(main())
