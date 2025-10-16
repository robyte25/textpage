from flask import Flask, request, jsonify, render_template_string
from g4f.client import Client

app = Flask(__name__)
client = Client()

html_template = """
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>TextPage KI</title>
  <style>
    body { font-family: sans-serif; background: #0f172a; color: white; display: flex; flex-direction: column; align-items: center; padding: 40px; }
    textarea { width: 90%; max-width: 600px; height: 120px; padding: 10px; border-radius: 10px; border: none; }
    button { margin-top: 10px; padding: 10px 20px; background: #2563eb; color: white; border: none; border-radius: 10px; cursor: pointer; }
    button:hover { background: #1e40af; }
    .output { margin-top: 20px; white-space: pre-wrap; background: #1e293b; padding: 20px; border-radius: 10px; width: 90%; max-width: 600px; }
  </style>
</head>
<body>
  <h1>TextPage — KI-Schreibassistent</h1>
  <form id="chatForm">
    <textarea name="prompt" placeholder="Schreibe hier deinen Text oder deine Frage..."></textarea>
    <button type="submit">Absenden</button>
  </form>
  <div class="output" id="output"></div>

  <script>
    const form = document.getElementById('chatForm');
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const prompt = form.prompt.value;
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt})
      });
      const data = await res.json();
      document.getElementById('output').textContent = data.response;
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
