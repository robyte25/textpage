from flask import Flask, request, jsonify, render_template_string
from g4f.client import Client

app = Flask(__name__)
client = Client()

html_template = """
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>TextPage KI — Dein Schreibassistent</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { box-sizing: border-box; transition: all 0.3s ease; }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(135deg, #0f172a, #1e293b);
      color: #f8fafc;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
      min-height: 100vh;
      padding: 40px 20px;
    }

    h1 {
      font-size: 2em;
      margin-bottom: 20px;
      text-align: center;
      color: #60a5fa;
      letter-spacing: 1px;
    }

    form {
      width: 100%;
      max-width: 650px;
      display: flex;
      flex-direction: column;
      align-items: center;
      background: rgba(30, 41, 59, 0.8);
      padding: 20px;
      border-radius: 16px;
      box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }

    textarea {
      width: 100%;
      height: 140px;
      resize: none;
      border: none;
      border-radius: 12px;
      padding: 14px;
      font-size: 1em;
      background: #1e293b;
      color: #e2e8f0;
      outline: none;
      margin-bottom: 12px;
    }
    textarea:focus {
      box-shadow: 0 0 0 3px #3b82f6;
    }

    button {
      background: #2563eb;
      border: none;
      color: white;
      padding: 12px 30px;
      font-size: 1em;
      border-radius: 12px;
      cursor: pointer;
      box-shadow: 0 4px 10px rgba(37,99,235,0.3);
    }
    button:hover {
      background: #1d4ed8;
      transform: translateY(-1px);
      box-shadow: 0 6px 12px rgba(37,99,235,0.5);
    }

    .output {
      margin-top: 30px;
      background: rgba(30,41,59,0.9);
      padding: 20px;
      border-radius: 16px;
      width: 100%;
      max-width: 650px;
      min-height: 100px;
      box-shadow: 0 0 15px rgba(0,0,0,0.3);
      white-space: pre-wrap;
      font-size: 1.05em;
      line-height: 1.6;
      animation: fadeIn 0.6s ease-in-out;
    }

    .loading {
      text-align: center;
      font-style: italic;
      color: #93c5fd;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  <h1>✨ TextPage — KI Schreibassistent</h1>
  <form id="chatForm">
    <textarea name="prompt" placeholder="Schreibe hier deinen Text, deine Idee oder Frage..."></textarea>
    <button type="submit">Absenden</button>
  </form>
  <div class="output" id="output"></div>

  <script>
    const form = document.getElementById('chatForm');
    const outputDiv = document.getElementById('output');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const prompt = form.prompt.value.trim();
      if (!prompt) return;
      outputDiv.innerHTML = "<div class='loading'>⏳ Text wird generiert...</div>";

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ prompt })
        });
        const data = await res.json();
        outputDiv.textContent = data.response || "❌ Keine Antwort erhalten.";
      } catch (err) {
        outputDiv.textContent = "⚠️ Fehler: " + err.message;
      }
    });
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content
    return jsonify({'response': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
