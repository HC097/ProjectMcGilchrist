from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/trickster", methods=["POST"])
def respond():
    data = request.json
    theme = data.get("theme", "[No theme provided]")
    response = f"The Trickster twists '{theme}' on its head, revealing hidden ironies, playful inversions, and paradoxes beneath the surface."
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=8104)
