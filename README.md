# WebChat
#### Video Demo:  <URL HERE>
#### Description:

What is this?
=============
A chat application where it's possible to jump into a chat room
with a random person.

Features
--------
- Chat anonymously with someone randomly assigned
- Go in a one on one chat where you're matched at random

Future
------
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

The Chat class (chat.py)
------------------------
I was noticing that I had a few global variables plus functions that acted upon it,
so what I thought was that it basicly was already a class only in a sloppy way.
This is now the Chat (and room) class which encapsulates all the logic and data for the different kinds of chat rooms.

With this, the creation of chat rooms is easy and the options I saw for generalizing made it possible to scale the size of a room however I see fit, so now creating bigger rooms is easy too, Yay!

**Why not add join_room from Flask-WebsocketIO?**
I think it could be a good idea to have a more centralized interface.
But I rather have it seperate at the moment, to make it look more like the docs make it out to be.

