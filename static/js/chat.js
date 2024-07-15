

const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);


const socket = new WebSocket('ws://' + window.location.host + '/ws/' + id + '/');

socket.onopen = function (e) {
    console.log("Connection Established", e);
}

socket.onclose = function (e) {
    console.log("Connection lost");
}
socket.onerror = function (e) {
    console.log(e);
}

socket.onmessage = function (e) {
    console.log(e);
    const data = JSON.parse(e.data);
    console.log(data);

    if (data.username == message_username) {
        document.querySelector('#chat-body').innerHTML += `
        <tr>
            <td>
                <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">
                    ${data.message} <br>
                    <small class="p-1  time-stamp">${data.timestamp}</small>
                </p>
            </td>
                               
        </tr>`
    }
    else {
        document.querySelector('#chat-body').innerHTML += `
        <tr>
            <td>
                <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">
                    ${data.message} <br>
                    <small class="p-1  time-stamp">${data.timestamp}</small>
                </p>
            </td>                                
        </tr>`
    }

}

function send_messagge(e) {
    console.log('button click');

    const message_input = document.querySelector("#message_input");
    const message = message_input.value;
    // const receiver = document.getElementById('json-username-receiver').textContent;
    if (message != '') {
        var currentTime = new Date();
        var options = { hour12: true };
        var timeString = currentTime.toLocaleTimeString([], options);
        socket.send(JSON.stringify({
            'message': message,
            'username': message_username,
            'timeStamp': timeString,

        }));
        message_input.value = '';
        // var chatWindow = document.getElementById("chat-window");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
    else {
        alert("Please enter a valid message")
    }
}

document.querySelector("#chat-message-submit").onclick = send_messagge


document.addEventListener('keydown', function(event) {
    if (event.key === "Enter") {
      // Call your function here
      send_messagge();
    }
  });
  



var chatWindow = document.getElementById("chat-window");
chatWindow.scrollTop = chatWindow.scrollHeight;
