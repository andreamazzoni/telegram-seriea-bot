from flask import Flask
from flask import request
from bot import run

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def receive():
    try:
        update = request.json
        run(update)
        return ""
    except Exception as e:
        print(e)
        return ""
