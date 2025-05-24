import os
# ... 其他程式碼 ...

def handle_audio(event):
    # ... 寫入音訊檔案 ...
    with open("temp_audio.m4a", "wb") as f:
        for chunk in audio_content.iter_content():
            f.write(chunk)

    try:
        text = transcribe_audio("temp_audio.m4a")
        summary = summarize_text(text)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=summary)
        )
    except Exception as e:
        print(f"處理語音時發生錯誤: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，語音轉文字或摘要服務發生問題。")
        )
    finally:
        # 確保臨時檔案被刪除
        if os.path.exists("temp_audio.m4a"):
            os.remove("temp_audio.m4a")