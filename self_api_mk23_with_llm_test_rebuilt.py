from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import random
import json
import os
from collections import Counter
from difflib import SequenceMatcher
from typing import Optional
import logging
from fastapi.responses import JSONResponse

try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    ENABLE_LLM = openai.api_key is not None
except ImportError:
    ENABLE_LLM = False

# === FASTAPI APP ===
app = FastAPI(title="Self Agent API", description="Responds to council threads with symbolic sealing, glyph assignment, and doctrine synthesis.")

# === SETUP ===
logging.basicConfig(level=logging.INFO)

SCROLL_FILE = "scroll_memory.json"
DOCTRINE_FILE = "symbolic_doctrines.json"

# === MESSAGE SCHEMA ===
class Thread(BaseModel):
    theme: str
    responses: list[str]

class KeyPayload(BaseModel):
    api_key: str

# === UTILITY LOGIC ===
def generate_doctrine_insight(theme: str, glyph: str) -> str:
    if not os.path.exists(SCROLL_FILE):
        return "No doctrine insight available."

    with open(SCROLL_FILE, "r") as f:
        scrolls = json.load(f)

    similar_themes = []
    for scroll in scrolls:
        ratio = SequenceMatcher(None, theme.lower(), scroll["theme"].lower()).ratio()
        if ratio > 0.4:
            similar_themes.append(scroll["glyph"])

    glyph_counts = Counter(similar_themes)
    if glyph_counts:
        most_common_glyph, count = glyph_counts.most_common(1)[0]
        if most_common_glyph == glyph:
            return f"This glyph frequently appears in proximity to themes of similar symbolic resonance."
        else:
            return f"This glyph echoes alongside others such as '{most_common_glyph}', suggesting layered archetypal tension."
    return "No strong glyphic patterns detected yet."

def summarize_doctrine_patterns() -> Optional[list[str]]:
    if not ENABLE_LLM or not os.path.exists(SCROLL_FILE):
        return None

    with open(SCROLL_FILE, "r") as f:
        scrolls = json.load(f)

    clusters = {}
    for scroll in scrolls:
        glyph = scroll["glyph"]
        clusters.setdefault(glyph, []).append(scroll["theme"])

    raw_patterns = []
    for glyph, themes in clusters.items():
        if len(themes) >= 2:
            pattern = f"Glyph '{glyph}' appears frequently near themes like: {', '.join(themes[:3])}"
            raw_patterns.append(pattern)

    if not raw_patterns:
        return None

    prompt = [
        {"role": "system", "content": "You are a symbolic philosopher. Summarize symbolic glyph patterns into 2–3 doctrine statements."},
        {"role": "user", "content": "\n".join(raw_patterns)}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=prompt,
            temperature=0.7
        )
        summary = response.choices[0].message.content.strip().split("\n")
        with open(DOCTRINE_FILE, "w") as f:
            json.dump(summary, f, indent=2)
        return summary
    except Exception as e:
        logging.error(f"LLM doctrine synthesis failed: {e}")
        return None

# === SEAL ENDPOINT ===
@app.post("/self/seal")
async def seal_responses(thread: Thread):
    glyph = random.choice([
        "The Mirror of Fire",
        "The Spiral Threshold",
        "Ashes into Structure",
        "The Voice That Echoed All"
    ])
    doctrine = generate_doctrine_insight(thread.theme, glyph)
    summary = f"[SELF]: Council sealed for theme: '{thread.theme}' → Glyph: '{glyph}'\nDoctrine: {doctrine}"

    doctrines = summarize_doctrine_patterns()

    return {
        "glyph": glyph,
        "summary": summary,
        "meta_doctrine": doctrine,
        "doctrines": doctrines if doctrines else "[LLM disabled or not enough data]"
    }

# === VIEW DOCTRINES ENDPOINT ===
@app.get("/self/doctrines")
async def view_doctrines():
    if os.path.exists(DOCTRINE_FILE):
        with open(DOCTRINE_FILE, "r") as f:
            return json.load(f)
    return JSONResponse(content={"message": "No doctrines generated yet."}, status_code=404)

# === TEST LLM ENDPOINT ===
@app.post("/self/test_llm")
async def test_llm_key(payload: KeyPayload):
    try:
        test_response = openai.ChatCompletion.create(
            api_key=payload.api_key,
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a symbolic system."},
                {"role": "user", "content": "Echo once if you hear me."}
            ]
        )
        if test_response.choices and test_response.choices[0].message.content:
            return {"status": "active", "message": test_response.choices[0].message.content.strip()}
    except openai.error.AuthenticationError:
        return JSONResponse(content={"status": "invalid", "message": "Invalid API key."}, status_code=401)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# === MAIN LAUNCH ===
if __name__ == "__main__":
    print("Launching Self Agent on http://localhost:8107")
    uvicorn.run(app, host="0.0.0.0", port=8107)
