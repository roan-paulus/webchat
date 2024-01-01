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
- Create an account and have your own username in chat.

Future
------
- Group conversations


Some Important Files
=====
run.sh
------
This sources config.env and allows it to make enviroment variables.
Then it runs the project.

app.py
-------
The meat of the application here you can find the main logic and all of the routes,
and sockets.

chat.py
-------
With this, the creation of chat rooms is easy and it should already be possible to create bigger rooms
then 1 one 1.

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

