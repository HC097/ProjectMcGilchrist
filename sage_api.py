
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# === FASTAPI APP ===
app = FastAPI(title="Sage Agent API", description="Responds to symbolic themes as the Sage archetype.")

# === MESSAGE SCHEMA ===
class Message(BaseModel):
    sender: str
    theme: str

# === SAGE LOGIC ===
@app.post("/sage/respond")
async def respond_sage(msg: Message):
    response = f"[SAGE]: In '{msg.theme}' echoes the teachings of silence, patience, and becoming."
    return {"response": response}

# === MAIN LAUNCH ===
if __name__ == "__main__":
    print("Launching Sage Agent on http://localhost:8105")
    uvicorn.run(app, host="0.0.0.0", port=8105)
