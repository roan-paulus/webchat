"""Run with run.sh for the needed enviroment variables"""
import os

from flask import (Flask, request, render_template, session,
                   redirect, flash)
from flask_socketio import SocketIO, send, join_room, leave_room

from chat import Chat
from reservedname import reserved_name_generator, is_name_reserved, RESERVED_NAME_START
from sql import SQLite, DATABASENAME
from utils import get_flashed_message, hash_password, logged_in


# Globals
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
socketio = SocketIO(app, logger=True, engineio_logger=True)

chat = Chat()
reserved_name = reserved_name_generator()


@socketio.on("connect")
def handle_connect(data):
    if "username" not in session:
        anonymous_username = next(reserved_name)
        session["username"] = anonymous_username


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
    session["room"].remove_user(request.sid)
    leave_room(session["room"], request.sid)
    send(f"{request.sid} has left the chat.", to=session["room"])


@socketio.on('disconnect')
def handle_disconnect():
    session["room"].remove_user(request.sid)
    leave_room(session["room"], request.sid)
    send(f"{session["username"]} has disconnected", to=session["room"])


@app.route("/")
def index():
    return render_template("index.html", flash_message=get_flashed_message(),
                           logged_in=logged_in(session))


@app.route("/chat", methods=["GET", "POST"])
def chatt():
    return render_template("chat.html", logged_in=logged_in(session))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").lower()

        with SQLite(DATABASENAME) as db:
            user = db.cursor.execute(
                "SELECT * FROM user WHERE username = ?", (username, )
            ).fetchone()

            if not user:
                flash("User not found.")
                return redirect("/login")

            password = request.form.get("password")
            if user["password_hash"] != hash_password(password, user["salt"]):
                raise Exception("WAAAA")
                flash("Incorrect password.")
                return redirect("/login")

        session["username"] = username
        flash(f"Welcome back {username}!")
        return redirect("/")

    return render_template("login.html", flash_message=get_flashed_message(),
                           logged_in=logged_in(session))


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username").lower()
    password = request.form.get("password")

    if is_name_reserved(username):
        flash(f"Names of {RESERVED_NAME_START} followed by a number are not allowed.")
        return redirect("/login")

    if not (username and password and password == request.form.get("pass-confirmation")):
        flash("Registration unsuccessful, please make sure you fill in all corresponding \
               fields and that your password confirmation matches your password.")
        return redirect("/login")

    with SQLite(DATABASENAME) as db:
        user_row = db.cursor.execute("SELECT * FROM user WHERE username = ?;",
                                     (username,)).fetchone()
        if user_row:
            flash(f"Username: {username} already exists.")
            return redirect("/login")

        salt = os.urandom(16).hex()
        hash = hash_password(password, salt)
        db.cursor.execute("""INSERT INTO user (username, password_hash, salt)
                                         VALUES (?, ?, ?)""",
                          (username, hash, salt))
        db.connection.commit()

    session["username"] = username
    flash("You're logged in.")
    return redirect("/")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You're logged out.")
    return redirect("/")


if __name__ == "__main__":
    files = os.listdir(os.path.dirname(__file__))

    if DATABASENAME not in files:
        with SQLite(DATABASENAME) as db, open("schema.sql") as schema:
            db.cursor.executescript(schema.read())

    socketio.run(app, host="0.0.0.0", debug=True)

