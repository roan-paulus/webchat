"""Run with run.sh for the needed enviroment variables"""
import os
import uuid

from flask import Flask, request, render_template, session, abort
from flask_socketio import SocketIO, send, join_room, leave_room
import requests


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
socketio = SocketIO(app, logger=True, engineio_logger=True)

chat_rooms = []


class User:
    def __init__(self, name) -> None:
        self.name = name


class BiChatRoom:
    def __init__(self) -> None:
        self.id: int = uuid.uuid4()
        self.users: list[str] = []
        self.full: bool = False

    def add_user(self, user: str) -> bool:
        if not self.full:
            self.users.append(user)
            if len(self.users) == 2:
                self.full = True

    def __str__(self):
        return f"BiChatRoom: {str(self.id)}"


@socketio.on("connect")
def handle_connect(data):
    if "username" not in session:
        resp = requests.get("https://randomuser.me/api/?format=json")
        random_username = resp.json()["results"][0]["name"]
        random_username = f"{random_username["first"]} {random_username["last"]}"

        session["username"] = random_username


@socketio.on('message')
def handle_message(data):
    send(f"{session["username"]}: {data["message"]}", to=1)


@socketio.on("join")
def handle_join(data):
    room = None
    for room in chat_rooms:
        if not room.full:
            room.add_user("TODO: What is a user?")
            room = room.id

    join_room(room, sid=request.sid)
    send({
        "sid": request.sid,
        "username": session["username"],
        "message": f"{session["username"]} has joined the chat.",
    }, to=room)


@socketio.on("leave")
def handle_leave(data):
    room = 1
    send(f"{request.sid} has left the chat.", to=room)


@socketio.on('disconnect')
def handle_disconnect():
    room = 1
    send(f"{session["username"]} has disconnected", to=room)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("chat.html")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)

