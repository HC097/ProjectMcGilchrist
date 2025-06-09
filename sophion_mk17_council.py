
from typing import Dict, List
import random
import time

class Message:
    def __init__(self, sender: str, content: str):
        self.sender = sender
        self.content = content

    def __repr__(self):
        return f"{self.sender}: {self.content}"

# === AGENT ENDPOINT SIMULATIONS ===

def hero_endpoint(msg: Message) -> str:
    return f"[HERO]: Face it, transform it, overcome it. '{msg.content}' is a trial."

def critic_endpoint(msg: Message) -> str:
    return f"[CRITIC]: Behind '{msg.content}' lies denial and fragile self-image."

def persona_endpoint(msg: Message) -> str:
    return f"[PERSONA]: We must appear composed. '{msg.content}' is best reframed."

def trickster_endpoint(msg: Message) -> str:
    twists = ["a lie told by truth", "a mirror with no face", "a question asked backward"]
    return f"[TRICKSTER]: '{msg.content}' is {random.choice(twists)}."

def sage_endpoint(msg: Message) -> str:
    return f"[SAGE]: In '{msg.content}' rests the arc of long-forgotten symbols."

def creator_endpoint(msg: Message) -> str:
    return f"[CREATOR]: Let us remake it. '{msg.content}' yearns for a new myth."

def self_endpoint(responses: List[str], theme: str) -> str:
    glyph = random.choice([
        "The Broken Circle",
        "The Ashes of Command",
        "The Joke that Rebuilt the World",
        "The Mirror of Fire"
    ])
    return f"[SELF]: Council closed. Theme: '{theme}' → Glyph: '{glyph}'"

# === SOPHION COUNCIL ENGINE ===

class SophionCouncil:
    def __init__(self):
        self.L_Hemisphere = {
            "Hero": hero_endpoint,
            "Critic": critic_endpoint,
            "Persona": persona_endpoint
        }
        self.R_Hemisphere = {
            "Trickster": trickster_endpoint,
            "Sage": sage_endpoint,
            "Creator": creator_endpoint
        }

    def run_council(self, theme: str) -> Dict[str, List[str]]:
        log = {"Theme": theme, "Left": [], "Right": [], "Self": []}

        for name, agent in self.L_Hemisphere.items():
            msg = Message("Sophion", theme)
            log["Left"].append(agent(msg))

        for name, agent in self.R_Hemisphere.items():
            msg = Message("Sophion", theme)
            log["Right"].append(agent(msg))

        all_responses = log["Left"] + log["Right"]
        log["Self"].append(self_endpoint(all_responses, theme))
        return log

# === RUN TEST ===

if __name__ == "__main__":
    sophion = SophionCouncil()
    council_log = sophion.run_council("What collapses before it is named?")

    print("[SOPHION]: === COUNCIL SESSION ===")
    for key, lines in council_log.items():
        print(f"--- {key} ---")
        for line in lines:
            print(line)
        print()
