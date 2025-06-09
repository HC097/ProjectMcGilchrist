
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import random

# === FASTAPI APP ===
app = FastAPI(title="Trickster Agent API", description="Responds to symbolic themes as the Trickster archetype.")

# === MESSAGE SCHEMA ===
class Message(BaseModel):
    sender: str
    theme: str

# === TRICKSTER LOGIC ===
@app.post("/trickster/respond")
async def respond_trickster(msg: Message):
    twist = random.choice([
        "a truth spoken by accident",
        "a game with no rules",
        "a door pretending to be a wall",
        "a mirror that winks back"
    ])
    response = f"[TRICKSTER]: '{msg.theme}' is {twist}."
    return {"response": response}

# === MAIN LAUNCH ===
if __name__ == "__main__":
    print("Launching Trickster Agent on http://localhost:8104")
    uvicorn.run(app, host="0.0.0.0", port=8104)
