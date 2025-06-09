
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# === FASTAPI APP ===
app = FastAPI(title="Creator Agent API", description="Responds to symbolic themes as the Creator archetype.")

# === MESSAGE SCHEMA ===
class Message(BaseModel):
    sender: str
    theme: str

# === CREATOR LOGIC ===
@app.post("/creator/respond")
async def respond_creator(msg: Message):
    response = f"[CREATOR]: '{msg.theme}' is not the end — it is material. Let us shape something unexpected from its ashes."
    return {"response": response}

# === MAIN LAUNCH ===
if __name__ == "__main__":
    print("Launching Creator Agent on http://localhost:8106")
    uvicorn.run(app, host="0.0.0.0", port=8106)
