"use strict"


let socket = io();

socket.on("connect", () => {
    socket.emit("join", {message: "User wants to join a room."});
});

// Add message to chat box
socket.on("message", (data) => {
    let msg = data["message"];
    const ud = "undefined";
    if (typeof msg === ud) {
        msg = data;
    }

    // Check socket IDs not undefined
    if (typeof socket.id === ud || typeof data["sid"] === ud) {
        console.error(`client socket id: ${socket.id} and server socket id: ${data["sid"]}`);
    }

    // Display message
    const msgBox = document.querySelector("#chat ul");

    let li = msgBox.appendChild(document.createElement("li"));
    if (socket.id === data["sid"]) {
        msg = `You've joined the chat as ${data["username"]}`;
    }
    li.textContent = msg;
});

// Submit and clear message box
const msgElement = document.querySelector("#message");
function msgSubmit(e) {
    e.preventDefault();

    const msg = msgElement.value;
    if (msg === "") {
        return false;
    }

    msgElement.value = "";
    msgElement.placeholder = "";

    socket.emit("message", {message: msg});
    return false;
}

