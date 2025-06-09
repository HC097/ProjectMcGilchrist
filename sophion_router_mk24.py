
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Persona endpoints
PERSONAS = {
    "creator": "http://localhost:8101/creator",
    "critic": "http://localhost:8102/critic",
    "sage": "http://localhost:8103/sage",
    "trickster": "http://localhost:8104/trickster",
    "hero": "http://localhost:8105/hero"
}

SELF_API_URL = "http://localhost:8108/self/glyph"  # Mk24 endpoint

@app.route("/route", methods=["POST"])
def route_to_personas():
    data = request.json
    theme = data.get("theme", "[No theme provided]")
    contributions = {}

    for name, url in PERSONAS.items():
        try:
            res = requests.post(url, json={"theme": theme})
            contributions[name] = res.json().get("response", "")
        except Exception as e:
            contributions[name] = f"[Error contacting {name}]"

    try:
        self_res = requests.post(SELF_API_URL, json={
            "theme": theme,
            "contributions": contributions
        })
        result = self_res.json()
    except Exception as e:
        result = {"error": str(e)}

    return jsonify(result)

if __name__ == "__main__":
    app.run(port=8100)
