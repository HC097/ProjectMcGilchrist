from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import random
import json
import os
from collections import Counter
from difflib import SequenceMatcher

# === FASTAPI APP ===
app = FastAPI(title="Self Agent API", description="Responds to council threads with symbolic sealing and glyph assignment, now with doctrine reflection.")

# === MESSAGE SCHEMA ===
class Thread(BaseModel):
    theme: str
    responses: list[str]

SCROLL_FILE = "scroll_memory.json"
META_FILE = "meta_doctrines.json"

# === SELF LOGIC ===
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

    return {
        "glyph": glyph,
        "summary": summary,
        "meta_doctrine": doctrine
    }

# === MAIN LAUNCH ===
if __name__ == "__main__":
    print("Launching Self Agent on http://localhost:8107")
    uvicorn.run(app, host="0.0.0.0", port=8107)
