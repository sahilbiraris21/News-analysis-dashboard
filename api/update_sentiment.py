import psycopg2
from transformers import pipeline

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="2105",  # change if different
    dbname="newsdb"
)
curr = conn.cursor()

# Load Hugging Face model
print("🧠 Loading sentiment model...")
sentiment_model = pipeline("sentiment-analysis")

# Fetch articles without valid sentiment
curr.execute("SELECT id, content FROM articles WHERE sentiment IS NULL OR sentiment = 0")
articles = curr.fetchall()

print(f"📰 Found {len(articles)} articles to analyze...")

for art_id, content in articles:
    if not content or not content.strip():
        continue

    # Analyze first 512 chars for performance
    result = sentiment_model(content[:512])[0]
    label, score = result["label"], result["score"]

    # Convert label to numeric
    sentiment = score if label == "POSITIVE" else -score

    # Update in DB
    curr.execute("UPDATE articles SET sentiment = %s WHERE id = %s", (sentiment, art_id))
    print(f"✅ Updated Article ID {art_id}: {label} ({sentiment:.2f})")

conn.commit()
curr.close()
conn.close()

print("🎉 All articles updated with real sentiment scores!")
