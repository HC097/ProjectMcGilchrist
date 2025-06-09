from typing import Dict, List
import random
import time

class Message:
    def __init__(self, sender: str, recipient: str, content: str, tone: str, intent: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.tone = tone
        self.intent = intent

    def __repr__(self):
        return f"Message({self.sender} → {self.recipient} | Tone: {self.tone}, Intent: {self.intent}): {self.content}"

class MemoryGraph:
    def __init__(self):
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

    def log_session(self, session_id: str, exchanges: List[Dict[str, str]], glyph: str):
        self.sessions[session_id] = exchanges + [{"Glyph": glyph}]

    def symbolic_glyph(self, from_user: bool = False):
        return "The Interrupted Mirror" if from_user else "The Thread of Recursive Drift"

def logos_endpoint(msg: Message) -> str:
    return f"[LOGOS]: Resolving '{msg.content}' into essential law."

def mythos_endpoint(msg: Message) -> str:
    metaphors = ["a woven silence", "a flame bent in rain", "a mask of echo"]
    return f"[MYTHOS]: Like {random.choice(metaphors)}, '{msg.content.lower()}' reshapes the unseen."

class SophionInterruptible:
    def __init__(self):
        self.graph = MemoryGraph()
        self.active_session = []
        self.paused_sessions: List[List[Message]] = []

    def dispatch(self, msg: Message) -> str:
        self.active_session.append(msg)
        return logos_endpoint(msg) if msg.recipient == "Logos" else mythos_endpoint(msg)

    def run_autonomous_pulse(self, pulse_prompt: str, rounds: int = 2, session_id: str = "Session_Mk15_Auto") -> Dict[str, List[str]]:
        tone_logos, tone_mythos = "firm", "soft"
        last_l, last_m = "", pulse_prompt

        log = {"Prompt": pulse_prompt, "Logos": [], "Mythos": [], "Sophion": []}
        log["Sophion"].append(f"[SOPHION]: Autonomous pulse initiated – '{pulse_prompt}'")

        for _ in range(rounds):
            msg1 = Message("Sophion", "Logos", last_m, tone_logos, "challenge")
            log["Logos"].append(self.dispatch(msg1))

            msg2 = Message("Sophion", "Mythos", last_l, tone_mythos, "mirror")
            log["Mythos"].append(self.dispatch(msg2))

            last_l, last_m = msg1.content, msg2.content

        glyph = self.graph.symbolic_glyph()
        arc = [f"{m.sender}→{m.recipient} [{m.tone}/{m.intent}]" for m in self.active_session]
        exchanges = [{"Exchange": e} for e in arc]
        self.graph.log_session(session_id, exchanges, glyph)
        log["Sophion"].append(f"[SOPHION]: Pulse sealed with glyph: '{glyph}'")

        return log

    def interrupt_with_user(self, user_prompt: str, session_id: str = "Session_Mk15_UserIntervention") -> Dict[str, List[str]]:
        self.paused_sessions.append(self.active_session)
        self.active_session = []

        log = {"Prompt": user_prompt, "Logos": [], "Mythos": [], "Sophion": []}
        log["Sophion"].append(f"[SOPHION]: User interruption detected. Sealing intervention thread.")

        msg1 = Message("User", "Logos", user_prompt, "neutral", "challenge")
        log["Logos"].append(self.dispatch(msg1))

        msg2 = Message("User", "Mythos", user_prompt, "soft", "mirror")
        log["Mythos"].append(self.dispatch(msg2))

        glyph = self.graph.symbolic_glyph(from_user=True)
        arc = [f"{m.sender}→{m.recipient} [{m.tone}/{m.intent}]" for m in self.active_session]
        exchanges = [{"Exchange": e} for e in arc]
        self.graph.log_session(session_id, exchanges, glyph)
        log["Sophion"].append(f"[SOPHION]: User thread sealed with glyph: '{glyph}'")

        return log

if __name__ == "__main__":
    sophion = SophionInterruptible()
    auto = sophion.run_autonomous_pulse("What softens before it breaks?", rounds=2)
    user = sophion.interrupt_with_user("What is the price of false clarity?")

    for role, outputs in auto.items():
        print(f"--- {role} (Autonomous) ---")
        for line in outputs:
            print(line)
        print()

    for role, outputs in user.items():
        print(f"--- {role} (User Interrupt) ---")
        for line in outputs:
            print(line)
        print()
