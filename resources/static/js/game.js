/**
 * Front end logic for the login panel.
 */

$(document).ready(() => {
    // Socket setup
    const socket = io();
    socket.on("connect", function() {
        // Set room id of socket
        const postParameters = {
            room_id: room_id
        };
        socket.emit("set-room", postParameters);
        socket.send("User has connected!");
    });
    socket.on("disconnect", function() {
        socket.send("User has disconnected!");
    });

    // Initialize the layout of the room
    socket.on("initialize-room", function (data) {
        blindsDisplay.innerHTML = "Current blinds: " + data.small + "/" + data.big;
        buyIn.value = data.buy_in;
    });
    socket.on("update-room", function (data) {
        // Do something
    });

    // General elements
    const start = document.getElementById("start-game");
    const sitDowns = document.getElementsByClassName("sit-down");
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

    for (var i = 0; i < sitDowns.length; i++) {
        sitDowns[i].onclick = sitDown;
    }
    function sitDown() {
        // Show all buttons
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
        doubleBlinds.style.visibility = "visible";
        blindsDisplay.style.visibility = "visible";
        sitOut.style.visibility = "visible";

        // Hide all other sit downs
        for (var i = 0; i < sitDowns.length; i++) {
            sitDowns[i].style.visibility = "hidden";
        }
        // Number of seat sat down on
        const seat = jQuery(this).attr("id").slice(-1);
    }

    start.onclick = startGame;
    function startGame() {

    }
});
