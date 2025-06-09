from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

MODELS = {
    "lh": "mistral",
    "rh": "openhermes",
    "cc": "tinyllama"
}

def call_ollama(model: str, prompt: str) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json().get("response", "[No response]")

def build_prompt(hemisphere: str, theme: str, contributions: dict) -> str:
    if hemisphere == "lh":
        voices = ["critic", "hero", "sage"]
        tone = "Analyze the theme using logical, critical, and heroic perspectives."
    elif hemisphere == "rh":
        voices = ["creator", "trickster", "sage"]
        tone = "Interpret the theme through myth, metaphor, and intuitive reflection."
    else:
        return ""

    relevant = [f"{role.title()}: {contributions.get(role, '')}" for role in voices if role in contributions]
    joined = "\n".join(relevant)
    return f"Theme: {theme}\n{tone}\n{joined}\nRespond with your insight."

@app.route("/self/glyph", methods=["POST"])
def generate_symbolic_response():
    data = request.json
    theme = data.get("theme", "[No theme provided]")
    contributions = data.get("contributions", {})

    # LH and RH prompts
    lh_prompt = build_prompt("lh", theme, contributions)
    rh_prompt = build_prompt("rh", theme, contributions)

    lh_response = call_ollama(MODELS["lh"], lh_prompt)
    rh_response = call_ollama(MODELS["rh"], rh_prompt)

    # Corpus callosum prompt
    cc_prompt = (
        f"Left Hemisphere says:\n{lh_response}\n\n"
        f"Right Hemisphere says:\n{rh_response}\n\n"
        "Synthesize these into a unifying insight or symbolic glyph."
    )
    glyph = call_ollama(MODELS["cc"], cc_prompt)

    return jsonify({
        "theme": theme,
        "lh": lh_response,
        "rh": rh_response,
        "glyph": glyph
    })

if __name__ == "__main__":
    app.run(port=8108)
