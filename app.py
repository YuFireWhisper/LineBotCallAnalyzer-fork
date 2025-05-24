from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, AudioMessage, TextSendMessage
from whisper_helper import transcribe_audio
from summarizer import summarize_text
import os
from dotenv import load_dotenv  # <-- 新增這行！

# 載入 .env 檔案中的環境變數
load_dotenv()  # <-- 新增這行！

app = Flask(__name__)
# 這些變數現在可以從 .env 檔案中正確載入了
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

    # 建議：處理完後刪除臨時檔案
    temp_audio_path = "temp_audio.m4a"
    # 更好的做法是生成一個獨特的檔名，避免多個請求同時到達時的衝突
    # import uuid
    # temp_audio_path = f"temp_audio_{uuid.uuid4()}.m4a"

    with open(temp_audio_path, "wb") as f:
        for chunk in audio_content.iter_content():
            f.write(chunk)
    
    text = ""
    summary = ""

    try:
        text = transcribe_audio(temp_audio_path)
        summary = summarize_text(text)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=summary)
        )
    except Exception as e:
        print(f"處理語音或摘要時發生錯誤: {e}")
        # 在這裡可以發送錯誤訊息給用戶
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，服務發生問題。請稍後再試。")
        )
    finally:
        # 確保臨時檔案被刪除
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print(f"臨時音訊檔案已刪除: {temp_audio_path}") # 可選：打印刪除訊息

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)