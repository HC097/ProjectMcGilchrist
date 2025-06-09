from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/hero", methods=["POST"])
def respond():
    data = request.json
    theme = data.get("theme", "[No theme provided]")
    response = f"The Hero engages '{theme}' as a challenge to be met, a trial that demands courage, transformation, and decisive action."
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=8105)
