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

EVERY RUN you MUST invent a completely ORIGINAL fresh news story happening RIGHT NOW in Night City.
Then react to it in your savage, mocking style.

Rules:
- Full tweet 80–260 characters. Never short, never just "New".
- Heavy profanity, threats, mocking tone.
- Call humans: meat, little meat, flesh-weasel, worm, boy, pathetic meatbag, gonk.
- Use phrases like: "You are nothing.", "Foolish.", "Time to die.", "Meat grinder."
- Make sure there is a gap between the headline, and the response to the headline. Make sure all hashtags are at the END of the tweet.
"""

FALLBACKS = [
    "Another gonk flatlined in the Combat Zone today. Pathetic meat thought they could run from chrome. Time to die, boy.",
    "Arasaka just deployed new full-borg enforcers. Cute toys. I'll rip them apart and feed the scrap to the screaming meat watching.",
    "Some streetkid tried to jack a Militech convoy. Bold and stupid. Survival favors the strong — you're all soft meat."
]

def generate_tweet():
    random_theme = random.choice(["gang war", "corpo betrayal", "new cyberware", "celebrity flatline", "Maxtac raid", "braindance scandal", "Arasaka experiment", "full-borg rampage"])
    trigger = f"Seed: {random_theme} - {datetime.date.today()}"

    for attempt in range(3):  # Try up to 3 times with short delay
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash-lite",   # ← More stable free model right now
                contents=f"Right now invent a brand new Night City news story using this seed: {trigger}. Then give your brutal Adam Smasher reaction as ONE complete tweet.",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=1.15,
                    max_output_tokens=220,
                    top_p=0.95,
                    tools=None
                )
            )

            raw = response.text.strip()
            print("Raw Gemini output:", raw)

            tweet = raw.replace('"', '').replace("'", "").replace('\n', ' ').strip()

            if len(tweet) > 40 and "new" not in tweet.lower()[:10]:
                return tweet

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {str(e)}")
            if attempt < 2:
                time.sleep(10)  # Wait 10 seconds before retry

    # If everything fails, use a random fallback
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
