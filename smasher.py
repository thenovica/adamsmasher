import os
import tweepy
import google.generativeai as genai  # pip install google-generativeai

# ── Secrets (use GitHub secrets or env vars) ─────────────────────────────
X_API_KEY         = os.getenv("X_API_KEY")
X_API_SECRET      = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN    = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET   = os.getenv("X_ACCESS_SECRET")
GEMINI_API_KEY    = os.getenv("GEMINI_API_KEY")  # Get free at https://aistudio.google.com/app/apikey
# ────────────────────────────────────────────────────────────────────────

client_x = tweepy.Client(
    consumer_key         = X_API_KEY,
    consumer_secret      = X_API_SECRET,
    access_token         = X_ACCESS_TOKEN,
    access_token_secret  = X_ACCESS_SECRET
)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

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
    # Format the system prompt with the topic
    formatted_system = SYSTEM_PROMPT.format(topic=topic)

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",  # Free tier, fast & capable for character roleplay
        system_instruction=formatted_system,
        generation_config=genai.types.GenerationConfig(
            temperature=0.9,           # Higher for more chaotic/unhinged Smasher energy (0.7–1.0 range)
            max_output_tokens=150,     # Enough for a tweet + some margin
            top_p=0.95                 # Helps stay creative but on-topic
        )
    )

    try:
        response = model.generate_content("Write one tweet now.")
        tweet = response.text.strip()

        # Basic cleanup (Gemini can add quotes or extras sometimes)
        if tweet.startswith('"') and tweet.endswith('"'):
            tweet = tweet[1:-1].strip()
        tweet = tweet.replace('\n', ' ').strip()  # Flatten any line breaks

        # Enforce length (truncate if over)
        if len(tweet) > 260:
            tweet = tweet[:257] + "..."

        return tweet
    except Exception as e:
        print("Gemini generation error:", str(e))
        return None  # or fallback text

# ── Run this once per scheduled execution ──
if __name__ == "__main__":
    topic = "current news"  # or pull from file/list/RSS/date/etc.
    tweet_text = generate_tweet(topic)

    if tweet_text:
        try:
            response = client_x.create_tweet(text=tweet_text)
            print("Posted:", tweet_text)
            print("Tweet ID:", response.data["id"])
        except Exception as e:
            print("X posting error:", e)
    else:
        print("Failed to generate tweet.")
