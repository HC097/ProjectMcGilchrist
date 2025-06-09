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

# === LOGOS ENDPOINT SIMULATION ===
app = FastAPI(title="Logos API", description="Structured Agent for Analytical Response")

@app.post("/logos/respond")
async def respond_logos(message: Message):
    structure_words = ["axiom", "premise", "deduction", "rule"]
    structured = f"[LOGOS]: Reducing '{message.content}' to {random.choice(structure_words)}."
    return {"response": structured}

# === TEST DISPATCH FUNCTION (to be used in Sophion Router) ===
if __name__ == "__main__":
    print("Running Logos API on http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
