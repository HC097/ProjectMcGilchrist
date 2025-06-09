
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# === FASTAPI APP ===
app = FastAPI(title="Hero Agent API", description="Responds to symbolic themes as the Hero archetype.")

# === MESSAGE SCHEMA ===
class Message(BaseModel):
    sender: str
    theme: str

# === HERO LOGIC ===
@app.post("/hero/respond")
async def respond_hero(msg: Message):
    response = f"[HERO]: Face it, transform it, overcome it. '{msg.theme}' is a trial."
    return {"response": response}

# === MAIN LAUNCH ===
if __name__ == "__main__":
    print("Launching Hero Agent on http://localhost:8101")
    uvicorn.run(app, host="0.0.0.0", port=8101)
