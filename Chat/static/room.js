var username = "";
function setUserName(username_) {
    username = username_;
}

const roomName = JSON.parse(document.getElementById("room-name").textContent);
const chatSocket = new ReconnectingWebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");
const chatSocket2 = new ReconnectingWebSocket("ws://" + window.location.host + "/ws/chat/" + "listener" + "/");

chatSocket2.onmessage = function (e) {
    var data = JSON.parse(e.data);

    for (let i in data["members_list"]) {
        if (data["members_list"][i] === username) {
            if (data["__str__"] !== username) {
                if (data["room_name"] !== roomName) {
                    if (!("Notification" in window)) {
                        alert("مرورگر شما از اعلان ها پشتیبانی نمی کند!");
                    } else if (Notification.permission === "granted") {
                        if (data["message_type"] === "txt") 
						var notification = new Notification(data["__str__"] + ": " + data["content"]);
                        else var notification = new Notification(data["__str__"] + ": عکس جدید");
                    } else if (Notification.permission !== "denied") {
                        Notification.requestPermission().then(function (permission) {
                            if (permission === "granted") {
                                var notification = new Notification("Hi there!");
                            }
                        });
                    }
                }
            }
        }
    }
};

chatSocket.onopen = function (e) {
    chatSocket.send(
        JSON.stringify({
            command: "fetch_message",
            room_name: roomName,
        })
    );
};

chatSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    if (data["command"] === "fetch_message") {
        for (let i = data["message"].length - 1; i >= 0; i--) {
            createMessage(data["message"][i]);
        }
    } else {
        createMessage(data);
    }
    let scorllNum = document.querySelector(".messages").scrollHeight;
    document.querySelector(".messages").scrollTop = scorllNum;
};

chatSocket.onclose = function (e) {
    document.querySelector("#chat-log").innerHTML = "";
    console.error("Chat socket closed unexpectedly");
};

document.querySelector("#chat-message-input").focus();
document.querySelector("#chat-message-submit").onclick = function (e) {
    let scorllNum = document.querySelector(".messages").scrollHeight;
    const messageInputDom = document.querySelector("#chat-message-input");
    let message = messageInputDom.value;
    if (message.replaceAll(" ", "")) {
        chatSocket.send(
            JSON.stringify({
                message: message,
                command: "new_message",
                username: username,
                room_name: roomName,
            })
        );
    }
    document.querySelector(".messages").scrollTop = scorllNum;
    messageInputDom.value = "";
};

document.getElementById("input-file").onclick = function (e) {
    document.getElementById("inp").click();
};

function createMessage(data) {
    var author = data["__str__"];
    var msgListTag = document.createElement("li");
    var imgTag = document.createElement("img");
	var convert_message = "";

    if (data["message_type"] === "img" || data["command"] === "img") {
        msgListTag = document.createElement("li");
        imgTag.src = data["content"];
        msgListTag.appendChild(imgTag);

        if (author === username) {
            msgListTag.classList.add("sent");
        } else {
            msgListTag.classList.add("replies");
        }

        document.querySelector("#chat-log").appendChild(msgListTag);
    } else {
		for (let i = 0; i < data["content"].split("\n").length; i++) {
			convert_message += `<p>${data["content"].split("\n")[i]}</p><br>`;
		}

        if (author === username) {
            msgListTag = `<li class='sent'><div>${convert_message}</div></li>`;
        } else {
            msgListTag = `<li class='replies'><div>${convert_message}</div></li>`;
        }

        document.querySelector("#chat-log").innerHTML += msgListTag;
    }
}

function readFile(e) {
    if (this.files && this.files[0]) {
        var FR = new FileReader();
        FR.addEventListener("load", function (e) {
            chatSocket.send(
                JSON.stringify({
                    content: e.target.result,
                    command: "img",
                    __str__: username,
                    room_name: roomName,
                })
            );
        });
        FR.readAsDataURL(this.files[0]);
    }
}

document.getElementById("inp").addEventListener("change", readFile);
