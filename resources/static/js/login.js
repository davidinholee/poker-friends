/**
 * Front end logic for the login panel.
 */

$(document).ready(() => {
    // Socket setup
    const socket = io();
    socket.on("connect", function() {
        socket.send("User has connected!");
    });
    socket.on("disconnect", function() {
        socket.send("User has disconnected!");
    });
    socket.on('redirect', function (data) {
        // Set cookies to save user information
        const d = new Date();
        // Cookies expire in a week
        d.setTime(d.getTime() + (7*24*60*60*1000));
        const expires = "expires="+ d.toUTCString();
        document.cookie = "username=" + data.username + ";" + expires + ";path=" + data.url;
        document.cookie = "userid=" + data.userid + ";" + expires + ";path=" + data.url;

        // Change to game window
        window.location = data.url;
        socket.disconnect();
    });
    socket.on('error', function (data) {
        roomError.innerHTML = "Room id does not exist.";
        loader.style.visibility = "hidden";
    });
    socket.on('error2', function (data) {
        createError.innerHTML = "Room creation failed. Please try again later.";
        loader.style.visibility = "hidden";
    });

    // General elements
    const joinTab = document.getElementById('join');
    const createTab = document.getElementById('create');
    const joinContent = document.getElementById('join-room');
    const createContent = document.getElementById('create-room');
    const tabContent = document.getElementsByClassName("tab-content");
    const tabLinks = document.getElementsByClassName("tab-links");
    const loginPanel = document.getElementById("login");
    const loader = document.getElementById("loader");
    // Join room tab elements
    const joinButton = document.getElementById('join-button');
    const roomID = $("#room-id");
    const roomIDLabel = document.getElementById('room-id-label');
    const roomIDForm = document.getElementById('room-id');
    const roomError = document.getElementById('room-id-error');
    const username = $("#username");
    const usernameLabel = document.getElementById('username-label');
    const usernameForm = document.getElementById('username');
    // Create room tab elements
    const createButton = document.getElementById('create-button');
    const username2 = $("#username2");
    const username2Label = document.getElementById('username2-label');
    const username2Form = document.getElementById('username2');
    const turnTime = document.getElementById("turn-time");
    const smallBlind = $("#small-blind");
    const bigBlind = $("#big-blind");
    const blindsLabel = document.getElementById('blinds-label');
    const smallBlindForm = document.getElementById('small-blind');
    const bigBlindForm = document.getElementById('big-blind');
    const createError = document.getElementById('create-error');
    const buyIn = $("#buy-in");
    const buyInLabel = document.getElementById('buy-in-label');
    const buyInForm = document.getElementById('buy-in');

    joinTab.onclick = openJoinTab;
    function openJoinTab() {
        // Get all elements with class="tab-content" and hide them
        for (let i = 0; i < tabContent.length; i++) {
            tabContent[i].style.display = "none";
        }

        // Get all elements with class="tab-links" and remove the class "active"
        for (let i = 0; i < tabLinks.length; i++) {
            tabLinks[i].className = tabLinks[i].className.replace(" active", "");
        }

        // Show the current tab, and add an "active" class to the button that opened the tab
        joinContent.style.display = "block";
        joinTab.className += " active";
        loginPanel.style.maxHeight = "70vh";
    }

    joinButton.onclick = joinRoom;
    function joinRoom() {
        // Room ID and Username validity checking.
        if (roomID.val() === "") {
            roomIDLabel.style.color = "#C10000";
            roomIDForm.style.borderBottom = "1px solid #C10000";
        } else {
            roomIDLabel.style.color = "black";
            roomIDForm.style.borderBottom = "1px solid black";
        }
        if (username.val() === "") {
            usernameLabel.style.color = "#C10000";
            usernameForm.style.borderBottom = "1px solid #C10000";
        } else {
            usernameLabel.style.color = "black";
            usernameForm.style.borderBottom = "1px solid black";
        }
        // Join room if it exists.
        if (roomID.val() !== "" && username.val() !== "") {
            const postParameters = {
                username: username.val(),
                room_id: roomID.val()
            };
            socket.emit("join-a-room", postParameters);
            loader.style.visibility = "visible";
        }
    }

    createTab.onclick = openCreateTab;
    function openCreateTab() {
        // Get all elements with class="tab-content" and hide them
        for (let i = 0; i < tabContent.length; i++) {
            tabContent[i].style.display = "none";
        }

        // Get all elements with class="tab-links" and remove the class "active"
        for (let i = 0; i < tabLinks.length; i++) {
            tabLinks[i].className = tabLinks[i].className.replace(" active", "");
        }

        // Show the current tab, and add an "active" class to the button that opened the tab
        createContent.style.display = "block";
        createTab.className += " active";
        loginPanel.style.maxHeight = "90vh";
    }

    createButton.onclick = createRoom;
    function createRoom() {
        // Blinds and Username validity checking.
        if (username2.val() === "") {
            username2Label.style.color = "#C10000";
            username2Form.style.borderBottom = "1px solid #C10000";
        } else {
            username2Label.style.color = "black";
            username2Form.style.borderBottom = "1px solid black";
        }
        if (smallBlind.val() === "" || bigBlind.val() === "") {
            blindsLabel.style.color = "#C10000";
            if (smallBlind.val() === "") {
                smallBlindForm.style.borderBottom = "1px solid #C10000";
            } else {
                smallBlindForm.style.borderBottom = "1px solid black";
            }
            if (bigBlind.val() === "") {
                bigBlindForm.style.borderBottom = "1px solid #C10000";
            } else {
                bigBlindForm.style.borderBottom = "1px solid black";
            }
        } else {
            blindsLabel.style.color = "black";
            smallBlindForm.style.borderBottom = "1px solid black";
            bigBlindForm.style.borderBottom = "1px solid black";
        }
        if (buyIn.val() === "") {
            buyInLabel.style.color = "#C10000";
            buyInForm.style.borderBottom = "1px solid #C10000";
        } else {
            buyInLabel.style.color = "black";
            buyInForm.style.borderBottom = "1px solid black";
        }

        // Create room if parameters are okay.
        let sB = smallBlind.val();
        let bB = bigBlind.val();
        let bI = buyIn.val();
        if (bI !== "" && sB !== "" && bB !== "" && username2.val() !== "") {
            if (isNaN(sB) || !(isPositiveInteger(sB))) {
                createError.innerHTML = "Small blind must be a positive integer.";
                blindsLabel.style.color = "#C10000";
                smallBlindForm.style.borderBottom = "1px solid #C10000";
            } else if (isNaN(bB) || !(isPositiveInteger(bB))) {
                createError.innerHTML = "Big blind must be a positive integer.";
                blindsLabel.style.color = "#C10000";
                bigBlindForm.style.borderBottom = "1px solid #C10000";
            } else if(parseInt(bB) < parseInt(sB)) {
                createError.innerHTML = "Big blind must be greater than small blind.";
                blindsLabel.style.color = "#C10000";
                bigBlindForm.style.borderBottom = "1px solid #C10000";
            } else if (isNaN(bI) || !(isPositiveInteger(bI))) {
                createError.innerHTML = "Buy in must be a positive integer.";
                buyInLabel.style.color = "#C10000";
                buyInForm.style.borderBottom = "1px solid #C10000";
            } else {
                const postParameters = {
                    username: username2.val(),
                    time: turnTime.options[turnTime.selectedIndex].value,
                    small: smallBlind.val(),
                    big: bigBlind.val(),
                    buy: buyIn.val()
                };
                socket.emit("create-room", postParameters);
                loader.style.visibility = "visible";
            }
        }
    }

    // Checks if a number is a positive integer.
    function isPositiveInteger(str) {
        const n = Math.floor(Number(str));
        return n !== Infinity && String(n) === str && n > 0;
    }

    // Open the assignments tab to start.
    openJoinTab();
});
