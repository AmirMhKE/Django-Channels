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

// Group list suggestion box

var search_input = document.querySelector("#room-search-input");
var suggestion_lists = document.querySelector(".group-lists");

search_input.addEventListener("input", () => {send_request(search_input.value)});

document.body.addEventListener("click", (e) => {
    if(e.target.id !== "room-search-input")
    suggestion_lists.style.display = "none"
});

search_input.addEventListener("focus", () => {
    if(suggestion_lists.innerHTML) { 
        suggestion_lists.style.display = "block";
    } else {
        suggestion_lists.innerHTML = "";
        suggestion_lists.style.display = "none";
    }
});

function send_request(value) {
    if(value) {
        fetch("/api/chats/?contains="+value).then(response => response.json())
        .then(data => set_suggestions_search_box(data));
    } else {
        suggestion_lists.innerHTML = "";
        suggestion_lists.style.display = "none";
    }
}

function set_suggestions_search_box(data) {
    suggestion_lists.innerHTML = "";
    suggestion_lists.style.display = "block";
    suggestion_lists.scrollTop = 0;

    for(let i=0; i < data.length; i++) {
        suggestion_lists.innerHTML += `
            <div class='group-item' data-group-name='${data[i]["group_name"]}'>
                <div class='row'>
                    <p class='col-6 text-right'>${data[i]["group_name"]}</p>
                    <p class='col-6 text-left'>${data[i]["members_count"]} 
                    <span><i class='fa fa-user'></i></span></p>
                </div>
            </div>
        `;
    }

    if(!data.length == 0) {
        var suggestion_items = document.querySelectorAll(".group-lists .group-item");

        for(i in suggestion_items) {
            try {
                suggestion_items[i].addEventListener("click", function() {
                    let group_name = this.getAttribute("data-group-name");
                    search_input.value = group_name;
                    suggestion_lists.innerHTML = "";
                    suggestion_lists.style.display = "none";
                });
            } catch {
                // ***
            }
        }
    } else {
        suggestion_lists.innerHTML = "";
        suggestion_lists.style.display = "none";
    }
}

// *****