from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/sage", methods=["POST"])
def respond():
    data = request.json
    theme = data.get("theme", "[No theme provided]")
    response = f"The Sage contemplates '{theme}' with timeless wisdom, balancing opposites and drawing on deep symbolic resonance."
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=8103)
