
import os
import requests
import json
from datetime import datetime
import traceback
from google import genai

GEMINI_API_KEY = ""
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

def send_telegram_message(message):
	url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
	payload = {
		"chat_id" : TELEGRAM_CHAT_ID,
		"text" : message,
#		"parse_mode": "Markdown"
	}

	try:
		response = requests.post(url, json=payload)
		response.raise_for_status()
		print("MESSAGE SUCCESS")
		return True
	except Exception as e:
		print(f"MESSAGE FAILURE: {e}")
		print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
		return False

def generate_econ_brief():
	client = genai.Client(api_key=GEMINI_API_KEY)
	model_name = "models/gemini-3-pro-preview"

	prompt = f"""

	You are an economics tutor helping a UK student prepare for their economics exam.
	Today's dtae is {datetime.now().strftime('%A, %B %d, %Y')}.

	Please create a daily economics brief with the following structure:

	**📊 KEY UK ECONOMIC METRICS**
	Find and report the current/latest values for:
	- UK CPI Inflation (%)
	- UK Unemployment Rate (%)
	- Bank of England Base Rate (%)
	- GBP/USD Exchange Rate
	- FTSE 100 Index

	**📰 OVERNIGHT ECONOMIC INSIGHTS (3-5 insights)**

	Search for the most recent UK economic news from the past 24-48 hours. Focus on:
	- Monetary policy (Bank of England decisions, interest rates)
	- Fiscal policy (government spending, taxation, budget)
	- Labour market changes
	- Trade and international economics
	- Major corporate/business news affecting the UK economy

	For each insight:
	1. Summarize the news/event briefly
	2. Explain the economic theory/concept it relates to (for exam application)
	3. Note potential exam question angles (e.g., "Could be asked about impact on AD/AS

	Format the entire response in clean, readable PLAIN TEXT (no Markdown, no asterisks for bold, no underscores). Use emojis sparingly for clarity. Keep it concise but exam-relevant.

	Focus on RECENT news (last 24-48 hours) and UK-specific content.
	DO NOT use any Markdown formatting (no **, __, etc). Use plain text only.

	IMPORTANT: Keep the total response under 3000 characters to fit in a Telegram message."""

	prompt = "whats the time and date, do you have a knowledge cutoff"
	try:
		response = client.models.generate_content(model=model_name, contents=prompt)
		if response.text:
			print("PROMPT SUCCESS")
			return response.text
		else:
			print("NO RESPONSED")
			return None
	except Exception as e:
		print(f"PROMPT FAILURE: {e}")
		traceback.print_exc()
		return None


def main():
	print(f"UK Economics Daily Brief - {datetime.now().strftime('%Y-%m-%d %H:%M')}")

	brief = generate_econ_brief()
	if brief:
		if len(brief) > 4000:
			brief = brief[:3900] + "\n\n [MESSAGE TRUNCATED"
		send_telegram_message(brief)
	else:
		send_telegram_message("ERROR GENERATING INSIGHTS")

if __name__ == "__main__":
	main()
