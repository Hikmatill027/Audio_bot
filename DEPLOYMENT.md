# Deployment Guide for Render

## Prerequisites

-   GitHub account with your bot code pushed
-   Render account (render.com)
-   Telegram Bot Token

## Step-by-Step Deployment

### 1. Prepare GitHub Repository

```bash
cd /Users/mac/Desktop/Python\ Projects/AudioBot
git init
git add .
git commit -m "Initial commit: AudioBot for Render deployment"
git branch -M main
git remote add origin https://github.com/yourusername/AudioBot.git
git push -u origin main
```

### 2. Create Render Account

-   Go to https://render.com
-   Sign up with GitHub account
-   Authorize Render to access your repositories

### 3. Deploy on Render

1. Click "New +" → "Web Service"
2. Select "Build and deploy from a Git repository"
3. Click "Connect" next to your AudioBot repository
4. Fill in the form:
    - **Name**: `audiobot` (or your preferred name)
    - **Root Directory**: Leave blank
    - **Runtime**: Python 3
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `python bot.py`
5. Click "Advanced" and add environment variables:
    - Key: `TELEGRAM_BOT_TOKEN`
    - Value: Your bot token from @BotFather
6. Select a plan (Free tier works for testing)
7. Click "Create Web Service"

### 4. Monitor Deployment

-   Go to your service dashboard
-   Check "Logs" to see if the bot is running
-   Wait for "Your service is live!" message

### 5. Verify Bot is Running

Test your bot on Telegram:

-   Search for your bot username
-   Send /start command
-   Verify it responds

### 6. Update Bot Webhook (if needed)

If using webhook instead of polling:

```bash
curl -F "url=https://audiobot-xxxx.onrender.com/" \
  https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook
```

## Troubleshooting

**Bot not responding:**

-   Check logs in Render dashboard
-   Verify TELEGRAM_BOT_TOKEN is set correctly
-   Ensure all dependencies in requirements.txt are correct

**Memory issues:**

-   Render free tier: 512 MB RAM (sufficient for this bot)
-   If needed, upgrade to paid plan

**Build fails:**

-   Check Python version (should be 3.10+)
-   Verify all imports in bot.py are in requirements.txt
-   Check for syntax errors

## Cost Considerations

-   **Free Tier**: 0.5 CPU, 512 MB RAM (good for testing)
-   **Paid Tier**: Starting at $7/month for more resources
-   No additional costs for Telegram API

## Auto-deploy

Render will automatically redeploy when you push to GitHub main branch.
