var socket = new WebSocket("ws://localhost:8000/ws");
let html = "";
var messageElement = document.getElementById("content");

socket.onopen = function(event) {
    console.log("WebSocket соединение установлено.");
};

socket.onmessage = function(event) {
    let message;  
    if (typeof event.data == "string") {
        message = event.data;
    } else {
        message = JSON.parse(event.data).message;  
    }
    displayMessage(message);  
};

socket.onclose = function(event) {
    console.log("WebSocket соединение закрыто.");
};

function displayMessage(message) {
  // Добавляем текст к существующему элементу
    html += message;
    messageElement.innerHTML += message;
    html = "";
}

socket.onmessage = function(event) {
    let data = event.data;
    displayMessage(data);   
}

const button = document.getElementById("send")
button.addEventListener("click", () => {
    const message = document.getElementById("message").value
    socket.send(message)
    }
)  