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
    audio_content = line_bot_api.get_message_content(message_id) # <-- audio_content 在這裡定義

    # 建議：處理完後刪除臨時檔案
    temp_audio_path = "temp_audio.m4a"
    with open(temp_audio_path, "wb") as f:
        for chunk in audio_content.iter_content():
            f.write(chunk)
    
    text = "" 
    summary = "" 

    try:
        text = transcribe_audio(temp_audio_path) # <-- 調用 whisper_helper 裡面的函式
        summary = summarize_text(text)           # <-- 調用 summarizer 裡面的函式

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=summary)
        )
    except Exception as e:
        print(f"處理語音或摘要時發生錯誤: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，服務發生問題。請稍後再試。")
        )
    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
