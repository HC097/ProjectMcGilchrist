from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/critic", methods=["POST"])
def respond():
    data = request.json
    theme = data.get("theme", "[No theme provided]")
    response = f"The Critic dissects '{theme}' to examine its structural integrity and logical implications, seeking precision and clarity."
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=8102)
