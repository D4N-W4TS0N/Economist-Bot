# 🇬🇧 UK Economics Daily Brief Bot

A Raspberry Pi-powered bot that sends AI-generated UK economics insights to your phone via Telegram every morning. Designed to help economics students practice applying theory to real-world scenarios.

## 📱 What It Does

Every morning at 6 AM, you receive a Telegram message containing:
- **Key UK Economic Metrics**: Inflation (CPI), unemployment rate, Bank of England base rate, GBP/USD exchange rate, FTSE 100
- **3-5 Economic Insights**: Recent UK economic developments with explanations of relevant economic theory and potential exam question angles
- **Exam-Focused Analysis**: Each insight connects economic concepts to practical applications for exam preparation

## ⚙️ Features

- ✅ **Completely Free**: Uses Google Gemini's free API tier
- ✅ **Automated Daily Delivery**: Runs via cron job at 6 AM
- ✅ **Telegram Integration**: Direct push notifications to your phone
- ✅ **Exam-Oriented**: Focuses on applying economic theory to real scenarios
- ✅ **Raspberry Pi**: Runs 24/7 on low-power hardware
- ✅ **Easy Setup**: Simple Python script with minimal dependencies

## ⚠️ Important Limitations

### Data Freshness
**The AI's training data only extends to early 2023.** This means:
- Economic metrics (inflation, base rate, etc.) are **not current**
- News and events are from **2023 or earlier**
- The bot **cannot** provide true "overnight" or "recent" news

### Why This Limitation Exists
- Google Gemini's free API does not include web search/grounding capabilities
- Real-time data access requires paid API tiers (Google AI or alternatives like Perplexity)
- The free tier is limited to the model's training cutoff date

### Is It Still Useful?
**Yes, for exam preparation!** Even with 2023 data, the bot is valuable for:
- **Practicing economic theory application** to real-world scenarios
- **Understanding economic concepts** through concrete examples
- **Exam question practice** by analyzing how events relate to theory
- **Daily study habit** formation with consistent morning briefings

### Workaround for Current Data
If you need current data, you have two options:
1. **Add free API integrations** (Bank of England, ONS, Alpha Vantage) to fetch real metrics, then let AI analyze them
2. **Upgrade to paid AI** with web search (Perplexity API ~$0.50/month, Claude API ~$1-2/month)

## 🛠️ Setup Instructions

### Prerequisites
- Raspberry Pi (any model with internet connection)
- Debian/Ubuntu-based OS (Raspberry Pi OS recommended)
- Python 3.13+
- Active internet connection

### 1. Create Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Save your **bot token** (looks like `123456789:ABCdef...`)
4. Message [@userinfobot](https://t.me/userinfobot) to get your **chat ID**

### 2. Get Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Save your API key (starts with `AIza...`)

### 3. Install on Raspberry Pi

```bash
# SSH into your Raspberry Pi
ssh user@raspberrypi.local

# Create project directory
mkdir ~/economics-bot
cd ~/economics-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install google-genai requests
```

### 4. Create the Script

Create `daily_brief.py`:

```bash
nano daily_brief.py
```

Paste the complete script (see `daily_brief.py` in this repository) and update these lines with your credentials:

```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID_HERE"
```

Save with `Ctrl+O`, then `Enter`, then exit with `Ctrl+X`.

### 5. Test the Script

```bash
python daily_brief.py
```

You should receive a message on Telegram within 10-20 seconds!

### 6. Schedule Daily Delivery

Set up a cron job to run at 6 AM daily:

```bash
crontab -e
```

Add this line:
```
0 6 * * * /home/YOUR_USERNAME/economics-bot/venv/bin/python /home/YOUR_USERNAME/economics-bot/daily_brief.py
```

Replace `YOUR_USERNAME` with your actual Raspberry Pi username.

Save and exit. The bot will now run automatically every morning at 6 AM!

## 📁 Project Structure

```
economics-bot/
├── venv/                  # Python virtual environment
├── daily_brief.py         # Main bot script
└── check_models.py        # (Optional) Check available Gemini models
```

## 🔧 Configuration

### Change Delivery Time

Edit your crontab:
```bash
crontab -e
```

Cron syntax: `minute hour day month weekday`

Examples:
- `0 6 * * *` - 6:00 AM daily
- `30 7 * * 1-5` - 7:30 AM weekdays only
- `0 8 * * 0` - 8:00 AM Sundays only

### Adjust Message Length

In `daily_brief.py`, modify the character limit (line ~68):

```python
IMPORTANT: Keep the total response under 3000 characters
```

Change `3000` to your preferred limit (Telegram max is 4096 characters).

### Change AI Model

The script uses `models/gemini-2.5-flash` by default. To try other models:

```bash
python check_models.py
```

Then update `model_name` in `daily_brief.py` (line ~31).

## 🐛 Troubleshooting

### "MESSAGE FAILURE: 400 Bad Request"
- Message is too long (>4096 chars) or has formatting errors
- Solution: Reduce character limit in prompt or disable Markdown parsing

### "PROMPT FAILURE: 404 NOT_FOUND"
- Invalid model name
- Solution: Check available models with `check_models.py`

### "429 RESOURCE_EXHAUSTED"
- Hit API rate limit
- Free tier limits: 15 requests/minute, generous daily quota
- Solution: Wait a few minutes and try again

### Bot doesn't send messages automatically
- Check cron is running: `systemctl status cron`
- Check cron logs: `grep CRON /var/log/syslog`
- Verify paths in crontab are absolute paths

### "TabError: inconsistent use of tabs and spaces"
- Mixed indentation in code
- Solution: Convert tabs to spaces:
```bash
expand -t 4 daily_brief.py > daily_brief_fixed.py
mv daily_brief_fixed.py daily_brief.py
```

## 📊 API Costs & Limits

### Google Gemini (Free Tier)
- **Cost:** $0/month
- **Rate Limits:** 15 requests/minute, 1,500 requests/day
- **Models:** gemini-2.5-flash, gemini-2.0-flash, and more
- **Limitations:** No web search, training data cutoff ~early 2023

### Telegram Bot API
- **Cost:** $0 (completely free)
- **Rate Limits:** Very generous (30 messages/second)

### Total Monthly Cost
**$0.00** - Completely free to run!

## 🔮 Future Improvements

Potential enhancements (pull requests welcome!):

- [ ] Add free API integrations for current UK economic data
- [ ] Support multiple recipients (send to multiple chat IDs)
- [ ] Web dashboard to view historical briefings
- [ ] Customizable topics (focus on specific areas like monetary policy)
- [ ] Option to request on-demand briefings (not just scheduled)
- [ ] Add charts/graphs for economic indicators
- [ ] Support for other countries/regions

## 🤝 Contributing

Contributions are welcome! Areas where help would be especially valuable:

1. **Free data source integrations** - Add APIs for current UK economic metrics
2. **Improved prompts** - Better AI prompts for more relevant exam insights
3. **Documentation** - Improve setup instructions or add troubleshooting tips
4. **Testing** - Test on different Raspberry Pi models or OS versions

## 📝 License

MIT License - feel free to use, modify, and distribute as you wish.

## ⚖️ Disclaimer

This bot is for **educational purposes only**. The economic data and insights provided:
- May not be current or accurate (training data cutoff ~early 2023)
- Should not be used for real financial or investment decisions
- Are AI-generated and may contain errors or biases
- Should be verified against official sources for exam preparation

Always cross-reference information with:
- [Bank of England](https://www.bankofengland.co.uk/)
- [Office for National Statistics (ONS)](https://www.ons.gov.uk/)
- Your course materials and textbooks

## 🙏 Acknowledgments

- Built with [Google Gemini API](https://ai.google.dev/)
- Powered by [Telegram Bot API](https://core.telegram.org/bots)
- Inspired by the need for daily economics exam practice

---

**Questions?** Open an issue or reach out!

**Found this helpful?** Star the repo ⭐
