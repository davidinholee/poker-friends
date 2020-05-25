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

    const a = getCookie("username");
    console.log(a);
});
