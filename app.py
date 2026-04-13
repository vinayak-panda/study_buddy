import os
import json
from groq import Groq
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/study", methods=["POST"])
def study():
    data = request.get_json()
    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({"error": "Please enter a topic."}), 400

    prompt = f"""You are an expert teacher and study coach.

The student wants to study: {topic}

Generate study material in this EXACT JSON format (no markdown, no backticks):
{{
  "topic": "<cleaned up topic name>",
  "summary": "<3-4 sentence overview of the topic>",
  "flashcards": [
    {{"question": "<question>", "answer": "<answer>"}},
    {{"question": "<question>", "answer": "<answer>"}},
    {{"question": "<question>", "answer": "<answer>"}},
    {{"question": "<question>", "answer": "<answer>"}},
    {{"question": "<question>", "answer": "<answer>"}}
  ],
  "quiz": [
    {{
      "question": "<multiple choice question>",
      "options": ["<option A>", "<option B>", "<option C>", "<option D>"],
      "answer": "<correct option letter A/B/C/D>",
      "explanation": "<why this is correct>"
    }},
    {{
      "question": "<multiple choice question>",
      "options": ["<option A>", "<option B>", "<option C>", "<option D>"],
      "answer": "<correct option letter A/B/C/D>",
      "explanation": "<why this is correct>"
    }},
    {{
      "question": "<multiple choice question>",
      "options": ["<option A>", "<option B>", "<option C>", "<option D>"],
      "answer": "<correct option letter A/B/C/D>",
      "explanation": "<why this is correct>"
    }},
    {{
      "question": "<multiple choice question>",
      "options": ["<option A>", "<option B>", "<option C>", "<option D>"],
      "answer": "<correct option letter A/B/C/D>",
      "explanation": "<why this is correct>"
    }},
    {{
      "question": "<multiple choice question>",
      "options": ["<option A>", "<option B>", "<option C>", "<option D>"],
      "answer": "<correct option letter A/B/C/D>",
      "explanation": "<why this is correct>"
    }}
  ]
}}"""

    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        text = response.choices[0].message.content
        text = text.strip().replace("```json", "").replace("```", "").strip()
        parsed = json.loads(text)
        return jsonify(parsed)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
