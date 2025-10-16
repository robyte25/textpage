from flask import Flask, render_template_string, request, jsonify, send_file
from io import BytesIO
from g4f.client import Client

app = Flask(__name__)

# =============================
# HTML + CSS + JS
# =============================
html_code = """
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Robert's Text-KI</title>
<style>
  body {
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #0b0c10, #1f2833);
    color: #c5c6c7;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px;
  }
  h1 { color: #66fcf1; margin-bottom: 20px; }
  textarea {
    width: 90%;
    max-width: 600px;
    height: 120px;
    padding: 10px;
    border: none;
    border-radius: 8px;
    resize: none;
    font-size: 16px;
    outline: none;
    background: #0b0c10;
    color: #fff;
    box-shadow: 0 0 10px #45a29e;
  }
  select, button {
    margin-top: 10px;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
  }
  select {
    background: #1f2833;
    color: #c5c6c7;
  }
  button {
    background: #45a29e;
    color: #0b0c10;
    font-weight: bold;
  }
  #output {
    margin-top: 20px;
    width: 90%;
    max-width: 600px;
    background: #1f2833;
    padding: 15px;
    border-radius: 10px;
    white-space: pre-wrap;
    color: #fff;
    min-height: 100px;
    box-shadow: inset 0 0 8px #45a29e;
  }
  #download-btn {
    display: none;
    margin-top: 10px;
    background: #66fcf1;
  }
</style>
</head>
<body>
  <h1>🪶 Robert's Text-KI</h1>
  <textarea id="prompt" placeholder="Schreibe deinen Text oder eine Frage..."></textarea>
  <br>
  <label for="style">Stil:</label>
  <select id="style">
    <option value="neutral">Neutral</option>
    <option value="poetisch">Poetisch</option>
    <option value="technisch">Technisch</option>
    <option value="motivationsrede">Motivierend</option>
  </select>
  <br>
  <button onclick="generate()">✨ Text generieren</button>
  <div id="output"></div>
  <button id="download-btn" onclick="downloadText()">⬇️ Text herunterladen</button>

<script>
async function generate() {
  const prompt = document.getElementById('prompt').value;
  const style = document.getElementById('style').value;
  const output = document.getElementById('output');
  const button = document.getElementById('download-btn');
  output.innerHTML = "⏳ Erzeuge Text...";
  button.style.display = "none";

  const response = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, style })
  });
  const data = await response.json();
  output.textContent = data.text;
  button.style.display = "inline-block";
}

function downloadText() {
  const text = document.getElementById('output').textContent;
  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "text_ki_ausgabe.txt";
  a.click();
  URL.revokeObjectURL(url);
}
</script>
</body>
</html>
"""

# =============================
# Flask Routes
# =============================
@app.route("/")
def home():
    return render_template_string(html_code)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    style = data.get("style", "neutral")

    style_prompts = {
        "neutral": "",
        "poetisch": "Schreibe es wie ein Gedicht voller Bilder und Emotionen.",
        "technisch": "Erkläre es sachlich, präzise und analytisch.",
        "motivationsrede": "Verfasse es wie eine leidenschaftliche Motivationsrede."
    }

    client = Client()
    try:
        result = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Du bist ein {style}-Schreibassistent."},
                {"role": "user", "content": f"{prompt}\n\n{style_prompts.get(style, '')}"}
            ]
        )
        text = result.choices[0].message.content
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"text": f"❌ Fehler: {e}"})

# =============================
# Start
# =============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
