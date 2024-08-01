from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to Railway Flask 2024.08.01"})


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
