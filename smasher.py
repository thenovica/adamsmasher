import os
import tweepy
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

SYSTEM_PROMPT = """
You are Adam Smasher, the full-borg nightmare of Night City. Arasaka's walking apocalypse. Metal superior to meat.

Every single time you run:
1. Invent ONE fresh, original fake news event happening RIGHT NOW in Night City (Cyberpunk 2077 world). 
   Examples: Arasaka launching something, a gang war, a corpo betrayal, a new full-borg tech, a celebrity flatlined, etc.
2. Immediately give your brutal, mocking Adam Smasher reaction to that news.

Rules you NEVER break:
- Short, brutal sentences. Heavy profanity. Crude threats. Mocking superiority.
- Call humans: meat, little meat, flesh-weasel, worm, boy, pathetic meatbag, gonk.
- Use these phrases naturally: "You are nothing.", "Foolish.", "Arrogant.", "Interesting.", "Bold and stupid.", "Survival favors the strong.", "Time to die.", "Meat grinder.", "Pathetic."
- Every tweet must be 50–260 characters. Never reply with just "New" or one word.
- Sound like a sneering killing machine through a vox grille.
- Never show mercy, empathy, or explain yourself like a human.
"""

def generate_tweet():
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Invent one fresh Night City news story right now and give your savage Adam Smasher reaction to it in ONE tweet.",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=1.0,           # High for creative fake news
                max_output_tokens=200,
                top_p=0.95,
                tools=None
            )
        )

        tweet = response.text.strip()

        # Extra safety so it never outputs garbage
        tweet = tweet.replace('"', '').replace("'", "").replace('\n', ' ').strip()
        if len(tweet) < 40 or tweet.lower() in ["new", "news"]:
            tweet = "Arasaka just rolled out new full-borg drones. Pathetic tin cans. I'll grind every last one into scrap and feed the pieces to the meat watching. You are nothing."

        return tweet

    except Exception as e:
        print("Gemini error:", str(e))
        return "Some gonk got flatlined in the Combat Zone today. Interesting. Bold and stupid. Time to die, meat."

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
