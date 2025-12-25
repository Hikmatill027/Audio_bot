# Til Talaffuzi Bot (Language Pronunciation Bot)

A Telegram bot that generates pronunciation audio for English and Korean words/phrases.

## Features

-   Support for English and Korean languages
-   Real-time audio generation using gTTS
-   Language switching
-   Uzbek interface

## Prerequisites

-   Python 3.10+
-   Telegram Bot Token (from @BotFather)
-   Render account

## Local Setup

1. Clone the repository

```bash
git clone https://github.com/yourusername/AudioBot.git
cd AudioBot
```

2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create .env file

```bash
echo "TELEGRAM_BOT_TOKEN=your_token_here" > .env
```

5. Run the bot

```bash
python bot.py
```

## Deployment to Render

See DEPLOYMENT.md for detailed instructions.
