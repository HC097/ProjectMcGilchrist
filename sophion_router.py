from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import asyncio
import json
import os
from datetime import datetime
from difflib import SequenceMatcher

app = FastAPI(title="Sophion Router Mk21", description="Dispatches symbolic themes to agents, seals them, reflects echoes, and stores scroll memory.")

SCROLL_FILE = "scroll_memory.json"
if not os.path.exists(SCROLL_FILE):
    with open(SCROLL_FILE, "w") as f:
        json.dump([], f)

class Theme(BaseModel):
    theme: str

AGENTS = {
    "Hero":     "http://localhost:8101/hero/respond",
    "Critic":   "http://localhost:8102/critic/respond",
    "Persona":  "http://localhost:8103/persona/respond",
    "Trickster":"http://localhost:8104/trickster/respond",
    "Sage":     "http://localhost:8105/sage/respond",
    "Creator":  "http://localhost:8106/creator/respond"
}
SELF_ENDPOINT = "http://localhost:8107/self/seal"

def find_best_echo(new_theme: str, scrolls: list) -> dict | None:
    best_match = None
    highest_ratio = 0.0
    for scroll in scrolls:
        ratio = SequenceMatcher(None, new_theme.lower(), scroll["theme"].lower()).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = scroll
    if highest_ratio >= 0.4:
        return {
            "theme": best_match["theme"],
            "glyph": best_match["glyph"],
            "summary": best_match["summary"]
        }
    return None

@app.post("/sophion/council")
async def run_council(theme: Theme):
    async with httpx.AsyncClient() as client:
        tasks = [client.post(url, json={"sender": "Sophion", "theme": theme.theme}) for url in AGENTS.values()]
        results = await asyncio.gather(*tasks)
        responses = [r.json()["response"] for r in results]

        seal_payload = {"theme": theme.theme, "responses": responses}
        seal = await client.post(SELF_ENDPOINT, json=seal_payload)
        seal_data = seal.json()

        with open(SCROLL_FILE, "r+") as f:
            data = json.load(f)
            echo = find_best_echo(theme.theme, data)

            scroll = {
                "theme": theme.theme,
                "responses": responses,
                "glyph": seal_data["glyph"],
                "summary": seal_data["summary"],
                "timestamp": datetime.now().isoformat(),
                "echo_from": echo
            }

            data.append(scroll)
            f.seek(0)
            json.dump(data, f, indent=2)

        return scroll

@app.get("/sophion/scrolls")
async def list_scrolls():
    with open(SCROLL_FILE, "r") as f:
        return json.load(f)

@app.get("/sophion/search")
async def search_scrolls(q: str):
    q = q.lower()
    with open(SCROLL_FILE, "r") as f:
        scrolls = json.load(f)
        results = [s for s in scrolls if q in s["theme"].lower() or q in s["glyph"].lower() or q in s["summary"].lower()]
        return results

if __name__ == "__main__":
    import uvicorn
    print("Launching Sophion Mk21 on http://localhost:8100")
    uvicorn.run(app, host="0.0.0.0", port=8100)
