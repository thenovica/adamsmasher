import os
import tweepy
import random
import datetime
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

# This forces a new random seed every run
random.seed(datetime.datetime.now().timestamp())

SYSTEM_PROMPT = """
You are Adam Smasher, the full-borg nightmare of Night City.

EVERY SINGLE RUN you MUST invent a completely new, original news event happening RIGHT NOW in Night City (never repeat anything you've said before).

Then give your savage, mocking reaction to it.

Rules:
- Short brutal sentences, heavy profanity, crude threats.
- Call humans: meat, little meat, flesh-weasel, worm, boy, pathetic meatbag, gonk.
- Use phrases like: "You are nothing.", "Foolish.", "Arrogant.", "Interesting.", "Bold and stupid.", "Time to die.", "Meat grinder."
- Tweet must be 80–260 characters. Never reply with just one word or "New".
- Always make the news feel fresh and different from any previous tweet.
"""

def generate_tweet():
    # Create a unique random trigger every run
    random_theme = random.choice([
        "gang war", "corpo betrayal", "new cyberware", "celebrity flatline",
        "Maxtac raid", "braindance scandal", "Arasaka experiment", "streetkid uprising",
        "full-borg incident", "netrunner heist", "trauma team failure", "fixer gone rogue"
    ])
    
    trigger = f"Random Night City chaos seed: {random_theme} on {datetime.date.today()}"

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Right now, invent a brand new Night City news story using this seed: {trigger}. Then give your brutal Adam Smasher reaction in ONE tweet.",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=1.1,          # Maximum creativity
                max_output_tokens=200,
                top_p=0.95,
                tools=None
            )
        )

        tweet = response.text.strip()

        # Final safety net
        tweet = tweet.replace('"', '').replace("'", "").replace('\n', ' ').strip()
        if len(tweet) < 50 or "new" in tweet.lower() and len(tweet) < 30:
            tweet = f"Another gonk flatlined in Watson today. Pathetic meat thought they could run from chrome. Time to die, boy. #NightCityMeatGrinder"

        return tweet

    except Exception as e:
        print("Gemini error:", str(e))
        return "Foolish meat. You are nothing. Time to die."

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
