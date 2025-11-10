import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import psycopg2
import psycopg2.extras
from transformers import pipeline
from scrapper.predict import DepartmentClassifier

# ---------------- INITIALIZE MODELS ---------------- #
department_model = DepartmentClassifier()

print("🧠 Loading Fake News Detection model... (this may take ~10s the first time)")
fake_news_detector = pipeline("text-classification", model="mrm8488/bert-tiny-finetuned-fake-news-detection")
print("✅ Fake News model loaded successfully!")

# ---------------- DATABASE CONNECTION ---------------- #
config = {
    "user": "postgres",
    "password": "2105",
    "host": "localhost",
    "dbname": "newsdb"
}

try:
    conn = psycopg2.connect(**config)
    print("✅ Connected to PostgreSQL database successfully!")
except Exception as e:
    print("❌ Database connection failed:", e)
    conn = None

# ---------------- FLASK SETUP ---------------- #
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
app.static_folder = "../client/out"

# ---------------- FRONTEND SERVING ---------------- #
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    """Serve static files from Next.js build (client/out)."""
    file_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

# ---------------- HEALTH CHECK ---------------- #
@app.route("/api/ping")
def ping():
    return {"status": "success", "data": "pong"}

# ---------------- GET ARTICLES (Paginated) ---------------- #
@app.route("/api/articles", methods=["GET", "POST"])
def get_articles():
    page = request.args.get("page", "0")
    limit = request.args.get("limit", "10")

    if not page.isnumeric() or not limit.isnumeric():
        return {"status": "fail", "data": "Invalid pagination params"}

    if not conn:
        return {"status": "fail", "data": "Database connection error"}

    try:
        curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        offset = int(page) * int(limit)

        curr.execute("""
            SELECT id, title, department, sentiment, created, content
            FROM articles
            ORDER BY created DESC
            LIMIT %s OFFSET %s;
        """, (int(limit), offset))

        data = curr.fetchall()
        curr.close()

        return {"status": "success", "data": data}
    except Exception as e:
        print("❌ Error in /api/articles:", e)
        return {"status": "fail", "data": str(e)}

# ---------------- GET SINGLE ARTICLE ---------------- #
@app.route("/api/getart", methods=["GET"])
def get_article_by_id():
    article_id = request.args.get("id")

    if not article_id or not article_id.isnumeric():
        return {"status": "fail", "data": "Invalid article ID"}

    if not conn:
        return {"status": "fail", "data": "Database connection error"}

    try:
        curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        curr.execute("""
            SELECT id, title, content, department, sentiment, created
            FROM articles
            WHERE id = %s;
        """, (article_id,))
        data = curr.fetchone()
        curr.close()

        if not data:
            return {"status": "fail", "data": "Article not found"}

        return {"status": "success", "data": data}
    except Exception as e:
        print("❌ Error in /api/getart:", e)
        return {"status": "fail", "data": str(e)}

# ---------------- FILTER BY SECTOR ---------------- #
@app.route("/api/filter", methods=["GET"])
def filter_articles():
    sector = request.args.get("sector")

    if not sector:
        return jsonify({"status": "fail", "message": "No sector provided"}), 400

    try:
        curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        curr.execute("""
            SELECT id, title, department, sentiment, created, content
            FROM articles
            WHERE LOWER(department) = LOWER(%s)
            ORDER BY created DESC
            LIMIT 50;
        """, (sector,))
        data = curr.fetchall()
        curr.close()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        print("❌ Error in /api/filter:", e)
        return jsonify({"status": "fail", "message": str(e)})

# ---------------- FAKE NEWS DETECTOR ---------------- #
@app.route("/api/fakenews", methods=["POST"])
def fake_news_check():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"status": "fail", "message": "No text provided"}), 400

        result = fake_news_detector(text[:512])
        print("🧩 Fake News Prediction:", result)

        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        print("❌ Error in /api/fakenews:", e)
        return jsonify({
            "status": "fail",
            "message": str(e)
        }), 500

# ---------------- DEPARTMENT + SENTIMENT CLASSIFIER ---------------- #
@app.route("/api/classify", methods=["POST"])
def classify_text():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"status": "fail", "message": "No text provided"}), 400

        result = department_model.inference(text)
        print("🔍 Classification Result:", result)
        return jsonify({"status": "success", "data": result})

    except Exception as e:
        print("❌ Error in /api/classify:", e)
        return jsonify({"status": "fail", "message": str(e)})

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001, debug=True)
