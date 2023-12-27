# ChatApp
#### Anonymously chat, one to one with other people.

How to run.
=============
1. Copy the output of:
`python3`
`uuid.uuid4().hex()`
2. Create a config.env file
3. Paste `FLASK_SECRET_KEY=<output>` (replace \<output\>) in that file
4. `pip install -r requirements.txt`
5. `./run.sh`


Features
--------
- Go in a one on one chat where you're matched at random.
- Create an account and have a username for chat.
- Chat without an account if desired.

Future
------
- Group conversations


Files
=====
run.sh
------
This sources config.env and allows it to make enviroment variables.
Then it runs the project.

config.env
----------
A not included file since it holds FLASK_SECRET_KEY for app.secret,
which is used for securely signing the session cookie.

.gitignore
----------
A file to tell git what files to ignore, this holds stuff like the above file,
cached and installed packages.

README.md
---------
This file!

app.py
-------
The meat of the application here you can find the main logic and all of the routes,
and sockets.

chat.py
-------
I was noticing that I had a few global variables plus functions that acted upon it,
so what I thought was that it basicly was already a class only in a sloppy way.
This is now the Chat (and room) class which encapsulates all the logic and data for the different kinds of chat rooms.

With this, the creation of chat rooms is easy and the options I saw for generalizing made it possible to scale the size of a room however I see fit, so now creating bigger rooms is easy too, Yay!

**Why not add join_room from Flask-WebsocketIO?**
I think it could be a good idea to have a more centralized interface.
But I rather have it seperate at the moment, to make it look more like the docs make it out to be.

requirement.txt
---------------
This holds all the dependencies this project needs.
Run `pip install -r requirements.txt` to install them!

schema.sql
----------
The schema for my database, here the user table is defined.
At the moment this is only used to save  and retrieve accounts.

sql.py
------
This holds a class to add a little spice to sqlite3.
I wanted to reduce some boilerplate and use pythons context manager
for this library.

sqlite3.db
----------
Another file not included but will be created automaticaly if the app starts.
Also schema.sql will run when this happens, so it will have tables too.

utils.py
--------
Some functions I don't know how to group yet, but also didn't want to pollute app.py with.
Contains a function that does a few repeated steps for hashing passwords,
a function that checks if you're logged in by passing a session and a shortcut to get just get
one flashed message, which I use a lot to give feedback to the user (for example if they logged
in succesfully or not).

static/
----------------------------------------
img/chat-app-logo-icon-vector.jpg
- This is just a file holding a stock image logo for my html pages.

script/event.js
- Holds all functions for interactivity on the site,
  like clicking away an info banner.
script/socketconnect.js
- This file combined with my sockets on the server allow me to create bi-directional connections.
  I kept this file intentionaly simple just to have control for what the user sees and have all
  complicated logic on the server

style/style.css
- Contains all the styles for my html pages
- I thought of splitting it up into more files but I was maybe a little lazy here. On the otherhand I knew it was gonna stay small like this.
- I decided not to use bootstrap to learn and struggle as much as I could about css in this project.

templates/
---------
chat.html
- The markup of my the page where you can chat with other people

index.html
- The main page where you can see what this application is.

layout.html
- This has the basic structure of every page there is.
- Is mainly the navigation bar

login.html
- Here you can login and register
Why login AND register? Because it could fit both and is still simple enough I think.


Why Websockets
==============
At first I thought of establishing a 'connection' by using http methods,
but soon this already started to proof unwieldy.
When I started googling I found the concept of Websockets and this was exactly what I needed.

A websocket would allow a bidirectional message channel from the client and the server.
With this I can have a smooth connection and not only that, (using Flask-SocketIO and it's 
dependencies) I could manage multiple of these channels at once.
Which also led me to the javascript Socket.IO library that plays nicely with my server.

