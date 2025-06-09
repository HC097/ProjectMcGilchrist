from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/creator", methods=["POST"])
def respond():
    data = request.json
    theme = data.get("theme", "[No theme provided]")
    response = f"The Creator perceives '{theme}' as a fertile space where new forms are waiting to emerge from symbolic potential."
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=8101)
