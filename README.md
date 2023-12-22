# Chat
#### Video Demo:  <URL HERE>
#### Description:

What is this?
=============
A chat application where it's possible to jump into a chat room
with a random person.

Features
--------
- Chat anonymously with someone randomly assigned

Future
------
- Go in a one on one chat where you're matched at random
- Create an account
- Group conversations
- Have options to stay connected after the conversation

Files
=====
- app.py
...


Design choices
==============
Websockets
----------
For my chat room I want users to be ablt to connect with eachother.<br>
The first objective would be one on one randomly assigned chat rooms.

At first I thought of establishing a 'connection' by using http methods,
but soon this already started to proof unwieldy.
When I started googling I found the concept of Websockets and this was exactly what I needed.

A websocket would allow a bidirectional message channel from the client and the server.
With this I can have a smooth connection and not only that, using Flask-SocketIO and it's 
dependencies could manage multiple of these channels at once.
Which also let me to the javascript Socket.IO library that plays nicely with my server.

