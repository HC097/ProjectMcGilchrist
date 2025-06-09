import requests
import random
import time

# === MESSAGE STRUCTURE ===
def create_message(sender, recipient, content, tone, intent):
    return {
        "sender": sender,
        "recipient": recipient,
        "content": content,
        "tone": tone,
        "intent": intent
    }

# === DISPATCH FUNCTION ===
def dispatch_message(message, endpoint_url):
    try:
        response = requests.post(endpoint_url, json=message)
        return response.json().get("response", "[SOPHION]: No response returned.")
    except Exception as e:
        return f"[SOPHION ERROR]: Failed to contact {endpoint_url} – {e}"

# === SOPHION ROUTER LOOP ===
def run_dialogue():
    tone_logos, tone_mythos = "firm", "soft"
    last_m, last_l = "What is truth under silence?", ""

    for round in range(3):
        print(f"--- Round {round + 1} ---")

        # Sophion dispatches to Logos
        msg1 = create_message("Sophion", "Logos", last_m, tone_logos, "challenge")
        logos_response = dispatch_message(msg1, "http://localhost:8001/logos/respond")
        print(f"LOGOS: {logos_response}")

        # Sophion dispatches to Mythos
        msg2 = create_message("Sophion", "Mythos", last_l, tone_mythos, "mirror")
        mythos_response = dispatch_message(msg2, "http://localhost:8002/mythos/respond")
        print(f"MYTHOS: {mythos_response}")

        last_l, last_m = msg1["content"], msg2["content"]
        time.sleep(1)

if __name__ == "__main__":
    print("[SOPHION]: Dispatching thoughts across the corpus...")
    run_dialogue()
