from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, AudioMessage, TextSendMessage
from whisper_helper import transcribe_audio
from summarizer import summarize_text
import os

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return "OK"

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
    message_id = event.message.id
    audio_content = line_bot_api.get_message_content(message_id)
    
    with open("temp_audio.m4a", "wb") as f:
        for chunk in audio_content.iter_content():
            f.write(chunk)
    
    text = transcribe_audio("temp_audio.m4a")
    summary = summarize_text(text)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=summary)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
