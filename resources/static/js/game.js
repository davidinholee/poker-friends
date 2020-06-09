/**
 * Front end logic for the login panel.
 */

$(document).ready(() => {
    // Socket setup
    const socket = io();
    socket.on("connect", function() {
        let user_id = getCookie("userid");
        if (user_id === "") {
            user_id = "0";
        }
        // Set room id of socket
        const postParameters = {
            room_id: room_id,
            user_id: user_id
        };
        socket.emit("set-room", postParameters);
        socket.send("User has connected!");
    });
    socket.on("disconnect", function() {
        socket.send("User has disconnected!");
    });

    // Redirect back to main page
    socket.on('redirect', function (data) {
        window.location = data.url;
        socket.disconnect();
    });

    // Initialize the layout of the room
    socket.on("initialize-room", function (data) {
        blindsDisplay.innerHTML = "Current blinds: " + data.small + "/" + data.big;
        buyIn.value = data.buy_in;

        // If new user, show login panel
        if (data.new_user) {
            login.style.visibility = "visible";
            loginPanel.style.animation = "0.5s ease-out 0s 1 popOut";
        }
        // If in game, show controls and hide sit downs
        if (data.in_game) {
            makeRightPanelVisible(data.started);
            console.log("Seat num: " + data.seat);
        }
        // Show each player currently in game
        for (let s in data.players) {
            // Set username and chips
            document.getElementById("name" + s).innerText = data.players[s][0];
            document.getElementById("chips" + s).innerText = data.players[s][1];
            // Make user visible
            document.getElementById("sit-down" + s).style.visibility = "hidden";
            document.getElementById("card" + s).style.visibility = "visible";
            document.getElementById("user" + s).style.animation = "0.4s ease-out 0s 1 popOut";
        }
    });

    // Set cookies to save user information
    socket.on("set-cookies", function (data) {
        const d = new Date();
        // Cookies expire in a week
        d.setTime(d.getTime() + (7*24*60*60*1000));
        const expires = "expires="+ d.toUTCString();
        document.cookie = "username=" + data.username + ";" + expires + ";path=" + data.url;
        document.cookie = "userid=" + data.userid + ";" + expires + ";path=" + data.url;
    });

    // New player has sat down at the table
    socket.on("new-player", function (data) {
        const s = data.seat;
        // Set username and chips
        document.getElementById("name" + s).innerText = data.username;
        document.getElementById("chips" + s).innerText = data.chips;
        // Make user visible
        document.getElementById("sit-down" + s).style.visibility = "hidden";
        document.getElementById("card" + s).style.visibility = "visible";
        document.getElementById("user" + s).style.animation = "0.4s ease-out 0s 1 popOut";
        if (data.started === "waiting") {
            waiting.style.visibility = "visible";
        } else if (data.started === "no") {
            start.style.visibility = "visible";
        }
    });

    // Show controls if game is to be started, display waiting message otherwise
    socket.on("enough-players", function (data) {
        if (data.not_enough) {
            start.style.visibility = "hidden";
            waiting.style.visibility = "visible";
        } else {
            start.style.visibility = "hidden";
            waiting.style.visibility="hidden";
            makeControlsVisible();
        }
    });

    socket.on("update-room", function (data) {
        //do something
    });

    // General elements
    const start = document.getElementById("start-game");
    const sitDowns = document.getElementsByClassName("sit-down");
    const login = document.getElementById("shade");
    const loginPanel = document.getElementById("login-panel");
    const username = document.getElementById("username");
    const join = document.getElementById("join-button")
    const waiting = document.getElementById("waiting");
    // Bottom panel elements
    const fold = document.getElementById("fold");
    const check = document.getElementById("check");
    const raise = document.getElementById("raise");
    const raisePot = document.getElementById("raise-bet");
    const lowerPot = document.getElementById("lower-bet");
    const slider = document.getElementById("bet-range");
    const output = document.getElementById("bet-display");
    const fourth = document.getElementById("fourth-pot");
    const half = document.getElementById("half-pot");
    const full = document.getElementById("full-pot");
    const allIn = document.getElementById("all-pot");
    // Right panel elements
    const buyInContainer = document.getElementById("buy-in-amount");
    const buyIn = document.getElementById("buy-in-actual");
    const doubleBlindsContainer = document.getElementById("double-blinds-container");
    const doubleBlinds = document.getElementById("double-blinds");
    const blindsDisplay = document.getElementById("blinds-display");
    const sitOut = document.getElementById("stand-up");
    const exit = document.getElementById("exit-room");

    // Get the cookie value of the cookie with name cname.
    function getCookie(cname) {
        const name = cname + "=";
        const decodedCookie = decodeURIComponent(document.cookie);
        const ca = decodedCookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) === 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    // Update the current slider value
    slider.oninput = function() {
        output.value = this.value;
    }
    // Display the default slider value
    output.innerHTML = slider.value;
    const a = getCookie("username");

    function makeRightPanelVisible(std) {
        // Show right panel
        doubleBlinds.style.visibility = "visible";
        blindsDisplay.style.visibility = "visible";
        sitOut.style.visibility = "visible";
        if (std === "no") {
            start.style.visibility = "visible";
        } else if (std === "waiting") {
            waiting.style.visibility = "visible";
        }

        // Hide all other sit downs
        for (var i = 0; i < sitDowns.length; i++) {
            sitDowns[i].style.visibility = "hidden";
        }
    }

    function makeControlsVisible() {
        // Show bottom panel
        fold.style.visibility = "visible";
        check.style.visibility = "visible";
        raise.style.visibility = "visible";
        raisePot.style.visibility = "visible";
        lowerPot.style.visibility = "visible";
        slider.style.visibility = "visible";
        output.style.visibility = "visible";
        fourth.style.visibility = "visible";
        half.style.visibility = "visible";
        full.style.visibility = "visible";
        allIn.style.visibility = "visible";
    }

    for (var i = 0; i < sitDowns.length; i++) {
        sitDowns[i].onclick = sitDown;
    }
    function sitDown() {
        makeRightPanelVisible();
        // Number of seat sat down on
        const seat = jQuery(this).attr("id").slice(-1);

        const postParameters = {
            user_id: getCookie("userid"),
            username: getCookie("username"),
            buy_in: buyIn.value,
            seat: seat,
            room_id: room_id
        };
        socket.emit("sit-down", postParameters);
    }

    join.onclick = makeUser;
    function makeUser() {
        const postParameters = {
            username: username.value,
            room_id: room_id
        };
        socket.emit("make-user", postParameters);
        login.style.visibility = "hidden";
    }

    start.onclick = startGame;
    function startGame() {
        const postParameters = {
            user_id: getCookie("userid"),
            username: username.value,
            room_id: room_id
        };
        socket.emit("start-game", postParameters);
    }
});
