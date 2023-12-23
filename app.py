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


class BiChatRoom:
    def __init__(self) -> None:
        self.id: str = str(uuid.uuid4())
        self.users: list[str] = []
        self.full: bool = False

    def add_user(self, user: str) -> None:
        if not self.full:
            self.users.append(user)
            if len(self.users) == 2:
                self.full = True

    def __str__(self):
        return f"BiChatRoom:{str(self.id)}"


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


def lookup_room() -> object:
    for room in chat_rooms:
        if not room.full:
            return room


@socketio.on("join")
def handle_join(data):
    room = lookup_room()
    if room is None:
        room = BiChatRoom()
        room.add_user(request.sid)
        chat_rooms.append(room)
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
    print("bye bye")
    send(f"{request.sid} has left the chat.", to=session["room"])


@socketio.on('disconnect')
def handle_disconnect(data):
    send(f"{session["username"]} has disconnected", to=session["room"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    return render_template("chat.html")


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)

