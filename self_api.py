
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import random

# === FASTAPI APP ===
app = FastAPI(title="Self Agent API", description="Responds to council threads with symbolic sealing and glyph assignment.")

# === MESSAGE SCHEMA ===
class Thread(BaseModel):
    theme: str
    responses: list[str]

# === SELF LOGIC ===
@app.post("/self/seal")
async def seal_responses(thread: Thread):
    glyph = random.choice([
        "The Mirror of Fire",
        "The Spiral Threshold",
        "Ashes into Structure",
        "The Voice That Echoed All"
    ])
    summary = f"[SELF]: Council sealed for theme: '{thread.theme}' → Glyph: '{glyph}'"
    return {"glyph": glyph, "summary": summary}

# === MAIN LAUNCH ===
if __name__ == "__main__":
    print("Launching Self Agent on http://localhost:8107")
    uvicorn.run(app, host="0.0.0.0", port=8107)
