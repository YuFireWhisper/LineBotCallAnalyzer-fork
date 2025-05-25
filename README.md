# 🎧 LINE 語音摘要機器人（Flask + Whisper + Gemini）

這是一個可以在 LINE 上接收語音訊息並回傳摘要的聊天機器人。使用 Flask 架設伺服器，搭配 Whisper 將語音轉文字，並使用 Google Gemini API 生成摘要內容。

本專案已重構為模組化架構，支援測試驅動開發（TDD），具備良好的可維護性和可擴展性。

---

## 🔧 功能架構

1. 使用者傳語音訊息至 LINE bot
2. Flask 伺服器接收並下載音訊
3. Whisper 轉換音檔為文字
4. Google Gemini 對文字進行摘要
5. LINE 回傳精簡重點內容

---

## 📦 技術棧

- **Python 3.8+** - 主要開發語言
- **Flask** - Web 框架
- **LINE Messaging API** - LINE Bot 整合
- **OpenAI Whisper** - 語音轉文字
- **Google Gemini API** - 文字摘要
- **pytest** - 單元測試框架
- **ABC (Abstract Base Classes)** - 介面抽象化

---

## 🏗️ 專案架構

```
LineBotCallAnalyzer-fork/
├── run.py                    # 應用程式入口點
├── app/                      # 主要應用程式目錄
│   ├── core/                 # 核心模組
│   │   ├── application.py    # Flask 應用程式工廠
│   │   ├── config.py         # 設定管理
│   │   ├── exceptions.py     # 自訂例外類別
│   │   └── interfaces.py     # 抽象基底類別
│   ├── handlers/             # 請求處理器
│   │   └── webhook_handler.py # LINE Webhook 處理器
│   ├── services/             # 業務邏輯服務
│   │   ├── transcription_service.py    # 語音轉錄服務
│   │   ├── summarization_service.py    # 文字摘要服務
│   │   ├── messaging_service.py        # LINE 訊息服務
│   │   ├── file_storage_service.py     # 檔案儲存服務
│   │   └── audio_analysis_workflow.py  # 音訊分析工作流程
│   └── utils/                # 工具函數
│       └── decorators.py     # 裝飾器
├── tests/                    # 測試目錄
│   ├── unit/                 # 單元測試
│   └── integration/          # 整合測試
├── run_tests.py             # 測試執行腳本
├── pytest.ini              # pytest 設定
├── Makefile                 # 自動化任務
└── requirements.txt         # Python 依賴套件
```

---

## 🚀 快速開始

### 1. 環境設定

```bash
# 複製專案
git clone <repository-url>
cd LineBotCallAnalyzer-fork

# 安裝依賴
pip install -r requirements.txt
# 或使用 Makefile
make install
```

### 2. 環境變數設定

建立 `.env` 檔案並設定以下變數：

```env
LINE_CHANNEL_ACCESS_TOKEN=你的LINE_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET=你的LINE_CHANNEL_SECRET
GEMINI_API_KEY=你的GEMINI_API_KEY
```

### 3. 執行應用程式

```bash
# 使用 Python
python run.py

# 或使用 Makefile
make run
```

---

## 🧪 測試

本專案採用測試驅動開發（TDD），提供完整的單元測試和整合測試：

```bash
# 執行所有測試
make test
# 或
python run_tests.py

# 只執行單元測試
make test-unit

# 只執行整合測試
make test-integration

# 使用 pytest（包含覆蓋率報告）
make test-pytest
```

---

## 🏛️ 架構設計原則

### 1. 依賴反轉原則 (Dependency Inversion)
- 使用抽象基底類別（ABC）定義介面
- 高階模組不依賴低階模組的具體實作
- 便於單元測試和模組替換

### 2. 單一職責原則 (Single Responsibility)
- 每個類別和函數都有明確、單一的職責
- 易於理解、測試和維護

### 3. 開閉原則 (Open/Closed)
- 對擴展開放，對修改封閉
- 新增功能時不需修改現有程式碼

### 4. 測試驅動開發 (TDD)
- 完整的單元測試和整合測試
- 確保程式碼品質和功能正確性

---

## 📝 開發指南

### 新增功能

1. 在 `app/core/interfaces.py` 定義抽象介面
2. 在 `app/services/` 實作具體服務
3. 在 `tests/unit/` 撰寫單元測試
4. 在 `tests/integration/` 撰寫整合測試
5. 更新 workflow 或 handler

### 程式碼品質

```bash
# 格式化程式碼
make format

# 檢查程式碼風格
make lint

# 執行所有檢查
make check
```

---

## 🐛 疑難排解

### 常見問題

1. **Whisper 模型載入失敗**
   - 確認系統有足夠記憶體
   - 嘗試使用較小的模型（如 "base"）

2. **Gemini API 調用失敗**
   - 檢查 API 金鑰是否正確
   - 確認 API 配額未超過限制

3. **LINE Webhook 驗證失敗**
   - 檢查 Channel Secret 是否正確
   - 確認 HTTPS 設定正確

---

## 🤝 貢獻指南

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 撰寫測試並確保通過
4. 提交變更 (`git commit -m 'Add some amazing feature'`)
5. 推送到分支 (`git push origin feature/amazing-feature`)
6. 開啟 Pull Request

---

## 📄 授權

此專案採用 MIT 授權條款。詳見 [LICENSE](LICENSE) 檔案。
