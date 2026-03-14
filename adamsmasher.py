import os
import tweepy
from groq import Groq  # pip install groq

# ── Secrets (use GitHub secrets or env vars) ─────────────────────────────
X_API_KEY         = os.getenv("Nqd6rMvhE3ZtSPdb4dPbjFhTO")
X_API_SECRET      = os.getenv("fkaB70okcffaESds1zfkURJXJoFmp69XwfPAlaoMw7EwYMbCFO")
X_ACCESS_TOKEN    = os.getenv("1694511724320243712-C5yvYAdKUj8pHYwhRcanC2Rpad2SNU")
X_ACCESS_SECRET   = os.getenv("v11th6jdxsWS2LzxtnsK6HdWxTMzKIJ3NDnRkviGd6HeW")

GROQ_API_KEY      = os.getenv("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")   # get free at console.groq.com/keys
# ────────────────────────────────────────────────────────────────────────

client_x = tweepy.Client(
    consumer_key         = X_API_KEY,
    consumer_secret      = X_API_SECRET,
    access_token         = X_ACCESS_TOKEN,
    access_token_secret  = X_ACCESS_SECRET
)

groq_client = Groq(api_key=GROQ_API_KEY)

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
- Topic to rant/smash about today: current News
Topic to tweet about today: {topic}
"""

def generate_tweet(topic="something random or from a list"):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(topic=topic)},
            {"role": "user",   "content": "Write one tweet now."},
        ],
        model="llama-3.1-70b-versatile",   # or mixtral, gemma2-27b, etc.
        temperature=0.8,   # 0.7–1.0 for more personality variation
        max_tokens=100,
    )
    tweet = chat_completion.choices[0].message.content.strip()
    # Clean up if needed (remove quotes, etc.)
    if tweet.startswith('"') and tweet.endswith('"'):
        tweet = tweet[1:-1]
    return tweet

# ── Run this once per scheduled execution ──
if __name__ == "__main__":
    topic = "current news"  # or pull from file/list/RSS
    tweet_text = generate_tweet(topic)
    
    try:
        response = client_x.create_tweet(text=tweet_text)
        print("Posted:", tweet_text)
        print("Tweet ID:", response.data["id"])
    except Exception as e:
        print("Error:", e)