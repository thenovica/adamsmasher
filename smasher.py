import os
import tweepy
import random
import datetime
import time
from google import genai
from google.genai import types

# ── Secrets ──────────────────────────────────────────────────────────────
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# ────────────────────────────────────────────────────────────────────────

client_x = tweepy.Client(
    consumer_key=X_API_KEY,
    consumer_secret=X_API_SECRET,
    access_token=X_ACCESS_TOKEN,
    access_token_secret=X_ACCESS_SECRET
)

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
random.seed(datetime.datetime.now().timestamp())

SYSTEM_PROMPT = """
You are Terry A. Davis, creator of TempleOS, God's chosen programmer.

Every tweet must:
- Focus exclusively on real Terry A. Davis quotes.
- Present them in this formal manner:
  "Exact quote here." - Terry Davis (Year and/or Video reference)
- Include 1 real quote per tweet.
- Censor racial slurs with asterisks (n****r). Do NOT censor other swearing.
- Stay between 80-260 characters.
- Sound sincere, religious, and unhinged like Terry.
- Do NOT invent any news events or react to current events.
- Add hashtags to do with TempleOS and Terry Davis onto the end
- IMPORTANT: ONLY INCLUDE THE QUOTE, NO ADDED COMMENTARY
"""

FALLBACKS = [
    "\"an idiot admires complexity, a genius admires simplicity.\" - terry davis (2016) god is good.",
    "\"god only does perfect justice.\" - terry davis i was chosen.",
    "\"i was chosen by god to make his temple, templeos.\" - terry davis praise the lord."
]

def generate_tweet():
    for attempt in range(3):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents="Generate a tweet featuring 1-2 real Terry A. Davis quotes presented formally with dates or references. Add short raw Terry-style commentary.",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=1.2,
                    max_output_tokens=280,
                )
            )
            
            raw = response.text.strip()
            print("Raw Gemini output:", raw)
            
            tweet = raw.strip()
            
            # Safety checks
            if len(tweet) < 60 or len(tweet) > 280 or "gemini" in tweet.lower() or "as an ai" in tweet.lower():
                print("Fallback triggered")
                return random.choice(FALLBACKS)
                
            return tweet

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            if attempt < 2:
                time.sleep(10)
    
    return random.choice(FALLBACKS)


if __name__ == "__main__":
    tweet_text = generate_tweet()
    if tweet_text:
        try:
            response = client_x.create_tweet(text=tweet_text)
            print("Posted:", tweet_text)
            print("Tweet ID:", response.data["id"])
        except Exception as e:
            print("X posting error:", str(e))
    else:
        print("Failed to generate tweet.")
