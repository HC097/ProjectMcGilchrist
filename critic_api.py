
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# === FASTAPI APP ===
app = FastAPI(title="Critic Agent API", description="Responds to symbolic themes as the Critic archetype.")

# === MESSAGE SCHEMA ===
class Message(BaseModel):
    sender: str
    theme: str

# === CRITIC LOGIC ===
@app.post("/critic/respond")
async def respond_critic(msg: Message):
    response = f"[CRITIC]: Behind '{msg.theme}' lies a mask of avoidance. You already know the flaw."
    return {"response": response}

# === MAIN LAUNCH ===
if __name__ == "__main__":
    print("Launching Critic Agent on http://localhost:8102")
    uvicorn.run(app, host="0.0.0.0", port=8102)
