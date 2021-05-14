document.querySelector("#room-search-input").onkeyup = function (e) {
    if (e.keyCode === 13) { // enter, return
        document.querySelector("#room-search-btn").click();
    }
};

document.querySelector("#room-create-input").onkeyup = function (e) {
    if (e.keyCode === 13) { // enter, return
        document.querySelector("#room-create-btn").click();
    }
};

document.querySelector("#room-search-btn").onclick = function (e) {
    var searchName = document.querySelector("#room-search-input").value;
    
    if(searchName.replaceAll(" ", "")) {
        window.location.pathname = "/chat/search/" + searchName.trim() + "/";
    } else {
        document.querySelector("#room-search-input").value = "";
    }
};

document.querySelector("#room-create-btn").onclick = function (e) {
    var groupName = document.querySelector("#room-create-input").value;
    
    if(groupName.replaceAll(" ", "")) {
        window.location.pathname = "/chat/" + groupName.trim() + "/create/confirm/";
    } else {
        document.querySelector("#room-create-input").value = "";
    }
};