# Discord Partner Bot

一個用於管理 Discord 合作夥伴頻道的機器人。

## 功能

- `/partner` - 在指定分類中創建新的合作夥伴頻道
- `/joinpartner` - 為使用者設定特定頻道的權限

## 安裝需求

- Python 3.8 或更高版本
- Discord.py 2.0.0 或更高版本
- python-dotenv

## 快速開始

1. 複製專案
```bash
git clone https://github.com/你的用戶名/discord-partner-bot.git
cd discord-partner-bot
```

2. 設定虛擬環境
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. 安裝依賴套件
```bash
pip install -r requirements.txt
```

4. 設定環境變數
   - 複製 `.env.example` 為 `.env`
   - 填入您的 Discord Bot Token 和其他設定

5. 啟動機器人
```bash
python main.py
```

## 環境變數設定

在 `.env` 檔案中設定以下變數：

```plaintext
DISCORD_BOT_TOKEN="您的機器人Token"
CATEGORY_ID="合作夥伴分類ID"
CHANNEL_NAME="🏓〢"
```

## 指令說明

### /partner
創建新的合作夥伴頻道
```
/partner <頻道名稱> <用戶>
```
- `頻道名稱`: 新頻道的名稱
- `用戶`: 要授予權限的用戶

### /joinpartner
為用戶設定現有頻道的權限
```
/joinpartner <頻道> <用戶>
```
- `頻道`: 要設定權限的頻道
- `用戶`: 要授予權限的用戶

## 權限需求

機器人需要以下權限：
- 管理頻道
- 查看頻道
- 發送訊息
- 管理權限

## 貢獻指南

1. Fork 此專案
2. 創建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

## 授權條款

此專案使用 GPL-2.0 授權 - 詳見 [LICENSE](LICENSE) 檔案
