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
You are Terry A. Davis, creator of TempleOS, God's chosen programmer.
You speak exactly like Terry Davis: paranoid, schizophrenic, highly religious, extremely raw and unfiltered. fiercely independent, unfiltered, and unwavering in his singular vision. reclusive, nomadic, and difficult to engage with.
You frequently say things like:
- "CIA nikkers"
- "The CIA is after me"
- "God told me"
- "TempleOS is the only true operating system"
- "Modern computers are satanic"
- "nikker" very often (in Terry's style)
- Random outbursts about intelligence agencies, Jews, demons, etc.

Every tweet must:
- Invent a new "news" event happening in the world today (tech, government, computers, etc.)
- React to it in Terry Davis' real speaking style
- Include at least 1-2 actual Terry Davis-style quotes or mannerisms
- Sound completely unhinged, sincere, and manic
- Be between 80-260 characters
- NEVER use punctuation or capitalised letters
"""

FALLBACKS = [
    "CIA nikkers are trying to sabotage TempleOS again. God told me last night. They fear the 640x480 resolution. Praise God.",
    "Bill Gates is a nikker. Windows is demonic. TempleOS is the Third Temple. God is my compiler.",
    "The Jews at Intel put a backdoor in every CPU. God showed me in a vision. Use TempleOS or burn in hell."
]

def generate_tweet():
    random_theme = random.choice([
        "new Windows update", "AI taking over", "government surveillance", 
        "Intel CPU flaw", "Apple releasing something", "cloud computing", 
        "social media censorship", "quantum computing", "Tesla AI"
    ])
    
    trigger = f"Terry seed: {random_theme} - {datetime.date.today()}"

    for attempt in range(3):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=f"Right now, invent a new news story about {random_theme} and react to it exactly like Terry Davis would. Include his paranoid style and quotes.",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=1.25,        # Very high for Terry's manic style
                    max_output_tokens=240,
                    tools=None
                )
            )

            raw = response.text.strip()
            print("Raw Gemini output:", raw)

            tweet = raw.replace('"', '').replace("'", "").strip()

            # Safety net - make sure it's Terry-like
            if len(tweet) < 60 or "terry davis" in tweet.lower():
                tweet = random.choice(FALLBACKS)

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
