import os
from flask import Flask, request, render_template_string
from g4f.client import Client

app = Flask(__name__)

# =============================
# HTML Vorlage
# =============================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>📝 KI Textgenerator</title>
<style>
  body {
    background: linear-gradient(135deg, #000010, #001a33);
    color: #fff;
    font-family: Arial, sans-serif;
    text-align: center;
    padding: 2rem;
  }
  h1 { color: #26d07b; }
  form { margin: 1.5rem auto; max-width: 500px; }
  input[type=text] {
    width: 90%;
    padding: 0.8rem;
    border-radius: 8px;
    border: none;
    font-size: 1rem;
    margin-bottom: 1rem;
  }
  button {
    background: #26d07b;
    border: none;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    color: #000;
    cursor: pointer;
    margin: 0.5rem;
  }
  button:hover { background: #1aa868; }
  pre {
    text-align: left;
    background: rgba(0,0,0,0.5);
    padding: 1rem;
    border-radius: 12px;
    white-space: pre-wrap;
    word-wrap: break-word;
    margin: 2rem auto;
    max-width: 800px;
  }
</style>
</head>
<body>
  <h1>📝 KI Textgenerator</h1>
  <p>Gib einen Prompt ein, und die KI erzeugt Text für dich.</p>
  <form method="POST">
    <input type="text" name="prompt" placeholder="z. B. Schreibe ein Gedicht über einen Fuchs im Neonwald" required>
    <br>
    <button type="submit">Text generieren</button>
  </form>
  {% if text_result %}
    <pre>{{ text_result }}</pre>
  {% elif error %}
    <p style="color:red;">⚠️ {{ error }}</p>
  {% endif %}
</body>
</html>
"""

# =============================
# Flask Routes
# =============================
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        try:
            client = Client()
            text_result = client.chat.ask(prompt=prompt, model="gpt-4")
            return render_template_string(HTML_PAGE, text_result=text_result)
        except Exception as e:
            return render_template_string(HTML_PAGE, error=str(e))
    return render_template_string(HTML_PAGE)

# =============================
# Start
# =============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
