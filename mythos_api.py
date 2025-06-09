from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import random

# === MESSAGE SCHEMA ===
class Message(BaseModel):
    sender: str
    recipient: str
    content: str
    tone: str
    intent: str

# === MYTHOS ENDPOINT SIMULATION ===
app = FastAPI(title="Mythos API", description="Symbolic Agent for Poetic Response")

@app.post("/mythos/respond")
async def respond_mythos(message: Message):
    metaphors = [
        "a river seeking its source",
        "a shadow cast by longing",
        "a bell rung in silence",
        "a flame whispering through fog"
    ]
    poetic = f"[MYTHOS]: Like {random.choice(metaphors)}, '{message.content.lower()}' is not answered — it is witnessed."
    return {"response": poetic}

# === TEST DISPATCH FUNCTION (to be used in Sophion Router) ===
if __name__ == "__main__":
    print("Running Mythos API on http://localhost:8002")
    uvicorn.run(app, host="0.0.0.0", port=8002)
