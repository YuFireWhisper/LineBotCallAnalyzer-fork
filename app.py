from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, AudioMessage

from whisper_helper import transcribe_audio
from summarizer import summarize_text
import os
from dotenv import load_dotenv
import uuid # 新增，用於生成唯一檔名

# 載入 .env 檔案中的環境變數
load_dotenv()

app = Flask(__name__)

# v3 版本的配置和 API 客戶端初始化
# 注意：v3 的 MessagingApi 和 WebhookHandler 不再直接接收 token 和 secret
# 而是在 Configuration 中設定，然後傳給 ApiClient
configuration = Configuration(
    access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
)

handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"處理 Webhook 錯誤: {e}")
        # 如果發生錯誤，通常返回 400 Bad Request
        abort(400)
    
    return "OK"

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
    message_id = event.message.id

    # 確保臨時檔案名是唯一的，以避免衝突
    temp_audio_path = f"temp_audio_{uuid.uuid4()}.m4a"

    try:
        # 使用 ApiClient 來取得內容
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            # 使用 get_message_content 方法
            with messaging_api.get_message_content(message_id) as audio_content:
                with open(temp_audio_path, "wb") as f:
                    for chunk in audio_content.iter_content():
                        f.write(chunk)
        
        text = transcribe_audio(temp_audio_path)
        summary = summarize_text(text)

        # 使用 v3 的 TextMessage 和 ReplyMessageRequest
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=summary)]
                )
            )
            print(f"回覆成功: {summary}")

    except Exception as e:
        print(f"處理語音或摘要時發生錯誤: {e}")
        # 在這裡可以發送錯誤訊息給用戶
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)
            messaging_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="抱歉，服務發生問題。請稍後再試。")]
                )
            )
    finally:
        # 確保臨時檔案被刪除
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print(f"臨時音訊檔案已刪除: {temp_audio_path}") # 可選：打印刪除訊息

if __name__ == "__main__":
    app.run(port=5000)