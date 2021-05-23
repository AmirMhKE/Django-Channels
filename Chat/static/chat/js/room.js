var username = document.getElementById("username").value;

const roomName = JSON.parse(document.getElementById("room-name").textContent);
const chatSocket = new ReconnectingWebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");
const chatSocket2 = new ReconnectingWebSocket("ws://" + window.location.host + "/ws/chat/" + "listener" + "/");

function scroll_to_down() {
    let scorllNum = document.body.scrollHeight;
    window.scrollTo(0, scorllNum);
}

function persian_number_converter(ls) {
    shapes = {"0": "۰", "1": "۱", "2": "۲", "3": "۳", "4": "۴", "5": "۵",
    "6": "۶", "7": "۷", "8": "۸", "9": "۹"};
    result = "";

    for(w of ls) {
        if(shapes[w] === undefined)
            result += w
        else
            result += shapes[w]
    }

    return result;
}

document.querySelector("#scroll-to-down").onclick = function() {
    scroll_to_down();
};

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
    document.querySelector("#chat-log").innerHTML = "";

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
        if(!data["message"].length == 0){ 
            for (let i = data["message"].length - 1; i >= 0; i--) {
                createMessage(data["message"][i]);
            }
            scroll_to_down();
        } else {
            document.querySelector("#chat-log").innerHTML = `
            <div class='no-message'>
                <h5>هیچ پیامی موجود نیست...</h5>
            </div>`;
        }
    } else {
        createMessage(data);
        scroll_to_down();
    }
};

chatSocket.onclose = function (e) {
    document.querySelector("#chat-log").innerHTML = `
    <div class='no-message'>
        <h5>اتصال اینترنت شما برقرار نیست...</h5>
    </div>`;
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
    var author = data["__str__"].split(" ")[0].trim();
    var msgListTag = document.createElement("li");
    var imgTag = document.createElement("img");
	var convert_message = "";

    if (data["message_type"] === "img" || data["command"] === "img") {
        msgListTag = document.createElement("li");
        imgTag.src = data["content"];
        imgTag.classList.add("msg-img");
        imgTag.setAttribute("loading", "lazy");
        msgListTag.appendChild(imgTag);

        if (author === username) {
            msgListTag.classList.add("sent");
        } else {
            msgListTag.classList.add("replies");
        }

        document.querySelector("#chat-log").appendChild(msgListTag);
        // message
        time = persian_number_converter(data["timestamp"].split("T")[1].split(".")[0]);
        date_m = data["timestamp"].split("T")[0].split("-");
        date_j = gregorian_to_jalali(Number(date_m[0]), Number(date_m[1]), Number(date_m[2]),);
        date_j = `${persian_number_converter(String(date_j[0]))}/${persian_number_converter(String(date_j[1]))}/${persian_number_converter(String(date_j[2]))}`;
        title = `
            <li class='${author === username ? "sent" : "replies"}'>
                <div class='msg-text'>
                    <h5>عکس ارسال شده از ${author === username ? "شما" : author}</h5>
                    <small>${date_j} | ${time}</small>
                </div>
            </li>
        `
        document.querySelector("#chat-log").innerHTML += title;
        // *****
    } else {
        convert_message = `<h5>${author === username ? "شما" : author}</h5>`;
		for (let i = 0; i < data["content"].split("\n").length; i++) {
			convert_message += `<p>${data["content"].split("\n")[i]}</p>`;
		}
        time = persian_number_converter(data["timestamp"].split("T")[1].split(".")[0]);
        date_m = data["timestamp"].split("T")[0].split("-");
        date_j = gregorian_to_jalali(Number(date_m[0]), Number(date_m[1]), Number(date_m[2]),);
        date_j = `${persian_number_converter(String(date_j[0]))}/${persian_number_converter(String(date_j[1]))}/${persian_number_converter(String(date_j[2]))}`;
        convert_message += `<small>${date_j} | ${time}</small>`;

        if (author === username) {
            msgListTag = `<li class='sent'><div class='msg-text'>${convert_message}</div></li>`;
        } else {
            msgListTag = `<li class='replies'><div class='msg-text'>${convert_message}</div></li>`;
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

// When scroll move to bottom hide top bar
var last_scroll_num = 0;
window.onscroll = function() {
    if(window.scrollY < last_scroll_num || window.scrollY <= 75)
        document.querySelector("header").style.display = "flex";
    else if(window.scrollY > last_scroll_num && window.scrollY > 75)
        document.querySelector("header").style.display = "none";

    last_scroll_num = window.scrollY;
};