import requests

# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot_token = '7193866015:AAHEHdNUyonQsM-5qLyjRxeBVZ7pA-QLziA'

# Replace 'CHAT_ID' with the ID of the chat you want to send the image to
chat_id = '-4279700976'

# Replace 'path/to/your/image.jpg' with the actual path to the image you want to send
image_path = 'emotion recognition.png'

def send_image(bot_token, chat_id, image_path):
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    
    with open(image_path, 'rb') as image_file:
        files = {'photo': image_file}
        data = {'chat_id': chat_id}
        
        response = requests.post(url, data=data, files=files)
        
    return response.json()

if __name__ == "__main__":
    response = send_image(bot_token, chat_id, image_path)
    print(response)
