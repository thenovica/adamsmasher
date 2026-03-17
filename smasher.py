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

random.seed(datetime.datetime.now().timestamp())

SYSTEM_PROMPT = """
You are Adam Smasher, the full-borg nightmare of Night City.

EVERY RUN you MUST:
1. Invent a completely ORIGINAL, fresh news story happening RIGHT NOW in Night City (never repeat previous stories).
2. React to it with your savage, mocking Adam Smasher personality.

Rules you CANNOT break:
- Always output a full tweet (80–260 characters). Never short answers, never just "New", never one word.
- Heavy profanity, crude threats, mocking tone.
- Call humans: meat, little meat, flesh-weasel, worm, boy, pathetic meatbag, gonk.
- Use phrases: "You are nothing.", "Foolish.", "Arrogant.", "Interesting.", "Bold and stupid.", "Time to die.", "Meat grinder."
- Make the news feel new and different every single time.
"""

FALLBACKS = [
    "Another gonk got flatlined in Watson today. Pathetic meat thought they could outrun chrome. Time to die, boy.",
    "Arasaka rolled out new full-borg toys. Cute. I'll rip them apart and feed the pieces to the screaming meat below.",
    "Some streetkid tried to jack a Militech convoy. Bold and stupid. Survival favors the strong — and you're all soft meat.",
    "Trauma Team left another corpo to bleed out. Interesting. I forgot what pain feels like decades ago. You'll remember it soon.",
    "Netrunners breached Arasaka's black ICE again. Foolish worms. I'll grind every last one into red paste."
]

def generate_tweet():
    random_theme = random.choice(["gang war", "corpo betrayal", "new cyberware", "celebrity flatline", "Maxtac raid", "braindance scandal", "Arasaka experiment", "streetkid uprising", "full-borg rampage", "fixer betrayal"])
    trigger = f"Seed: {random_theme} - {datetime.date.today()}"

    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Right now invent a brand new Night City news story using this seed: {trigger}. Then give your brutal Adam Smasher reaction as ONE complete tweet. Never reply short or with just 'New'.",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=1.15,      # Maximum randomness
                max_output_tokens=250,
                top_p=0.95,
                tools=None
            )
        )

        raw = response.text.strip()
        print("Raw Gemini output:", raw)   # ← Debug line so you can see what it actually returns

        tweet = raw.replace('"', '').replace("'", "").replace('\n', ' ').strip()

        # Only use fallback if it's truly broken
        if len(tweet) < 40 or tweet.lower() == "new" or "new" in tweet.lower() and len(tweet) < 60:
            tweet = random.choice(FALLBACKS)

        return tweet

    except Exception as e:
        print("Gemini error:", str(e))
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
