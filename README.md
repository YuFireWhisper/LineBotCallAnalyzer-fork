# 🎧 LINE 語音摘要機器人（Flask + Whisper + OpenAI）

這是一個可以在 LINE 上接收語音訊息並回傳摘要的聊天機器人。使用 Flask 架設伺服器，搭配 Whisper 將語音轉文字，並使用 OpenAI API 生成摘要內容。

---

## 🔧 功能架構

1. 使用者傳語音訊息至 LINE bot
2. Flask 伺服器接收並下載音訊
3. Whisper 轉換音檔為文字
4. OpenAI GPT 對文字進行摘要
5. LINE 回傳精簡重點內容

---

## 📦 技術棧

- [Python 3.8+]
- [Flask]
- [LINE Messaging API](https://developers.line.biz/)
- [OpenAI GPT-3.5/4](https://platform.openai.com/)
- [OpenAI Whisper](https://github.com/openai/whisper)
- Docker（部署 n8n 自動流程，選用）
