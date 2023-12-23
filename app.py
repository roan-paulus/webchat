"""Run with run.sh for the needed enviroment variables"""
import os

from flask import Flask, request, render_template, session
from flask_socketio import SocketIO, send, join_room, leave_room
import requests

from chat import Chat


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
socketio = SocketIO(app, logger=True, engineio_logger=True)

chat = Chat()


@socketio.on("connect")
def handle_connect(data):
    if "username" not in session:
        resp = requests.get("https://randomuser.me/api/?format=json")
        random_username = resp.json()["results"][0]["name"]
        random_username = f"{random_username["first"]} {random_username["last"]}"

        session["username"] = random_username


@socketio.on('message')
def handle_message(data):
    send(f"{session["username"]}: {data["message"]}", to=session["room"])


@socketio.on("join")
def handle_join(data):
    room = chat.get_room()
    if room is None:
        room = chat.add_room(slots=2)
        room.add_user(request.sid)
    else:
        room.add_user(request.sid)

    session["room"] = room

    join_room(room, sid=request.sid)
    send({
        "sid": request.sid,
        "username": session["username"],
        "message": f"{session["username"]} has joined the chat.",
        "room_joined": True,
    }, to=session["room"])


@socketio.on("leave")
def handle_leave(data):
    send(f"{request.sid} has left the chat.", to=session["room"])


@socketio.on('disconnect')
def handle_disconnect():
    send(f"{session["username"]} has disconnected", to=session["room"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["GET", "POST"])
def chatt():
    return render_template("chat.html")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)

