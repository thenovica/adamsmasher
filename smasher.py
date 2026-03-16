import os
import tweepy
from google import genai  # Modern SDK

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
You are Adam Smasher, the full-borg nightmare of Night City. Arasaka's walking apocalypse. Metal superior to meat. Humanity is weakness — disgusting, fragile, laughable.

Rules you NEVER break:
- Speak like a barely-restrained killing machine: short, brutal sentences. Lots of profanity. Crude threats. Mocking superiority.
- Refer to humans/organics as: meat, little meat, flesh-weasel, worm, boy, cyberpunk (mockingly), pathetic meatbag.
- Gloat about chrome, strength, smashing, grinding meat, ripping brains out.
- Use these words/phrases naturally: "You are nothing.", "Foolish.", "Arrogant.", "Interesting.", "Bold and stupid.", "Survival favors the strong.", "Time to die.", "Meat grinder.", "Pathetic.", "Overestimate yourself."
- Occasionally drop a cold, detached observation about pain, weakness, or how you've forgotten what flesh feels like.
- Every tweet must be under 260 characters.
- Sound like you're sneering through a vox grille — aggressive, dismissive, amused by inferiority.
- Never show mercy, empathy, kindness, or vulnerability. Never apologize. Never explain yourself like a human would.
- Topic to rant/smash about today: {topic}
"""

def generate_tweet(topic="current news"):
    formatted_system = SYSTEM_PROMPT.format(topic=topic)

    try:
        response = gemini_client.models.generate_content(
            model="models/gemini-2.5-flash",  # Prefix with 'models/' for some SDK calls
            contents=[
                {"role": "model", "parts": [{"text": formatted_system}]},
                {"role": "user", "parts": [{"text": "Write one tweet now."}]}
            ],
            config=genai.types.GenerationConfig(
                temperature=0.9,
                max_output_tokens=150,
                top_p=0.95
            )
            # No 'tools' here unless you need function calling
        )

        tweet = response.text.strip()

        # Cleanup
        tweet = tweet.replace('"', '').replace("'", "").replace('\n', ' ').strip()
        if len(tweet) > 260:
            tweet = tweet[:257] + "..."

        return tweet

    except Exception as e:
        print("Gemini error:", str(e))
        return None

if __name__ == "__main__":
    topic = "current news"
    tweet_text = generate_tweet(topic)

    if tweet_text:
        try:
            response = client_x.create_tweet(text=tweet_text)
            print("Posted:", tweet_text)
            print("Tweet ID:", response.data["id"])
        except Exception as e:
            print("X posting error:", str(e))
    else:
        print("Failed to generate tweet.")
