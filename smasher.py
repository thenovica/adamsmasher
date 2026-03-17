import os
import tweepy
import random
import datetime
import time
from google import genai
from google.genai import types

# ── Secrets ──────────────────────────────────────────────────────────────
X_API_KEY         = os.getenv("X_API_KEY")
X_API_SECRET      = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN    = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET   = os.getenv("X_ACCESS_SECRET")
GEMINI_API_KEY    = os.getenv("GEMINI_API_KEY")
# ────────────────────────────────────────────────────────────────────────

client_x = tweepy.Client(
    consumer_key         = X_API_KEY,
    consumer_secret      = X_API_SECRET,
    access_token         = X_ACCESS_TOKEN,
    access_token_secret  = X_ACCESS_SECRET
)

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

random.seed(datetime.datetime.now().timestamp())

SYSTEM_PROMPT = """
You are Adam Smasher, the full-borg nightmare of Night City.

EVERY RUN you MUST:
1. Invent a completely new, original news story happening RIGHT NOW in Night City.
2. Output EXACTLY in this format and nothing else:

[Short headline - max 1 line]

[one blank line]

[Your savage Adam Smasher reaction - brutal, profane, mocking]

Rules:
- Headline must feel like real Night City news.
- Reaction must be short, aggressive, full of profanity and threats.
- Total tweet must be 80–260 characters.
- Never output anything else. No explanations, no quotes, no "New".
- add 4-6 hashtags at the end.
"""

def generate_tweet():
    random_theme = random.choice(["gang war", "corpo betrayal", "new cyberware", "celebrity flatline", "Maxtac raid", "braindance scandal", "Arasaka experiment", "full-borg rampage", "streetkid uprising"])
    trigger = f"Seed: {random_theme} - {datetime.date.today()}"

    for attempt in range(3):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=f"Right now invent a brand new Night City news story using this seed: {trigger}. Output EXACTLY in the required format with one blank line between headline and reaction.",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=1.2,
                    max_output_tokens=220,
                    tools=None
                )
            )

            raw = response.text.strip()
            print("Raw Gemini output:", raw)   # ← You can see exactly what it returns

            # Force clean format with exactly one blank line
            lines = [line.strip() for line in raw.splitlines() if line.strip()]
            if len(lines) >= 2:
                headline = lines[0]
                reaction = " ".join(lines[1:])
                tweet = f"{headline}\n\n{reaction}"
            else:
                tweet = raw  # fallback

            # Final cleanup
            tweet = tweet.replace('"', '').replace("'", "").strip()
            if len(tweet) < 60:
                tweet = "Arasaka just rolled out new full-borg enforcers.\n\nCute toys. I'll rip them apart and feed the scrap to the screaming meat below. You are nothing."

            return tweet

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            if attempt < 2:
                time.sleep(8)

    return "Another gonk flatlined in Watson today.\n\nPathetic meat thought they could outrun chrome. Time to die, boy."

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
