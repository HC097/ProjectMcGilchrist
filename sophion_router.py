
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import asyncio

# === FASTAPI APP ===
app = FastAPI(title="Sophion Router API", description="Dispatches symbolic themes to all archetypal agents and seals them with the Self.")

# === THEME INPUT ===
class Theme(BaseModel):
    theme: str

# === AGENT ENDPOINTS ===
AGENTS = {
    "Hero":     "http://localhost:8101/hero/respond",
    "Critic":   "http://localhost:8102/critic/respond",
    "Persona":  "http://localhost:8103/persona/respond",
    "Trickster":"http://localhost:8104/trickster/respond",
    "Sage":     "http://localhost:8105/sage/respond",
    "Creator":  "http://localhost:8106/creator/respond"
}
SELF_ENDPOINT = "http://localhost:8107/self/seal"

# === ROUTE: COUNCIL SESSION ===
@app.post("/sophion/council")
async def run_council(theme: Theme):
    async with httpx.AsyncClient() as client:
        tasks = []
        for name, url in AGENTS.items():
            payload = {"sender": "Sophion", "theme": theme.theme}
            tasks.append(client.post(url, json=payload))

        results = await asyncio.gather(*tasks)
        responses = [r.json()["response"] for r in results]

        seal_payload = {"theme": theme.theme, "responses": responses}
        seal = await client.post(SELF_ENDPOINT, json=seal_payload)
        seal_data = seal.json()

        return {
            "theme": theme.theme,
            "responses": responses,
            "glyph": seal_data["glyph"],
            "summary": seal_data["summary"]
        }

# === RUN SERVER ===
if __name__ == "__main__":
    import uvicorn
    print("Launching Sophion Router on http://localhost:8100")
    uvicorn.run(app, host="0.0.0.0", port=8100)
