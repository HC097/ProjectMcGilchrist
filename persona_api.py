
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# === FASTAPI APP ===
app = FastAPI(title="Persona Agent API", description="Responds to symbolic themes as the Persona archetype.")

# === MESSAGE SCHEMA ===
class Message(BaseModel):
    sender: str
    theme: str

# === PERSONA LOGIC ===
@app.post("/persona/respond")
async def respond_persona(msg: Message):
    response = f"[PERSONA]: We maintain the mask not to deceive, but to survive. '{msg.theme}' must appear beautiful."
    return {"response": response}

# === MAIN LAUNCH ===
if __name__ == "__main__":
    print("Launching Persona Agent on http://localhost:8103")
    uvicorn.run(app, host="0.0.0.0", port=8103)
