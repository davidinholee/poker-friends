from flask import Flask, render_template, url_for, request, make_response, redirect
from flask_socketio import SocketIO, send, emit
import firebase_admin
from firebase_admin import credentials, db
import string
import random
import uuid
import datetime

# Create a Firebase application
cred = credentials.Certificate("./poker-friends-d6d1a-firebase-adminsdk-ao0t2-7568eee8c7.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://poker-friends-d6d1a.firebaseio.com'
})
ref = db.reference("/")
rooms = ref.child('rooms')
users = ref.child('users')

# Create app with template and routes folders pointed to correct locations
app = Flask(__name__, template_folder="resources/templates/", static_folder="resources/static/")
app.config["SECRET_KEY"] = "mysecret"
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html",
                           font_url1="https://fonts.googleapis.com/css?family=Amaranth",
                           font_url2="https://fonts.googleapis.com/css?family=Averia Libre",
                           socket_url="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.3/socket.io.js",
                           error=" ")


@app.route('/<id>')
def game(id):
    name = request.cookies.get('userid')
    print(name)
    return render_template("game.html",
                           font_url1="https://fonts.googleapis.com/css?family=Amaranth",
                           font_url2="https://fonts.googleapis.com/css?family=Averia Libre",
                           socket_url="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.3/socket.io.js")


@socketio.on("message")
def handle_message(msg):
    print("Message:", msg)


@socketio.on('create-room')
def create_room(json):
    room_data = rooms.get()
    user_data = users.get()
    day = int(datetime.datetime.now().day)

    # Create unique room id.
    alphnum = string.ascii_lowercase + string.digits
    room_id = ''.join((random.choice(alphnum) for i in range(6)))
    i = 0

    if room_data is not None:
        while True:
            if not(room_id in room_data):
                break
            elif i > 1000:
                # If somehow not enough unique room ids, just return back to login
                return render_template("index.html",
                                       font_url1="https://fonts.googleapis.com/css?family=Amaranth",
                                       font_url2="https://fonts.googleapis.com/css?family=Averia Libre",
                                       socket_url="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.3/socket.io.js",
                                       error="Room creation failed. Please try again later.")
            i += 1

        # Clean up rooms database.
        for key in room_data:
            created = int(room_data[key]["created"])
            if (created + 1 < day) or (created >= 28 and day > 1 and day < 28):
                if len(room_data[key]['users']) == 0:
                    rooms.child(key).delete()

    if user_data is not None:
        # Clean up users database.
        created = int(user_data[key]["created"])
        if (created + 1 < day) or (created >= 28 and day > 1 and day < 28):
            if len(user_data[key]['active_room']) == "":
                users.child(key).delete()

    # Create unique user id
    user_id = str(uuid.uuid1())

    # Update database with new information
    rooms.child(room_id).set({"users": [],
                              "time_limit": json["time"],
                              "small": json["small"],
                              "big": json["big"],
                              "buy_in": json["buy"],
                              "admin": user_id,
                              "created": datetime.datetime.now().day})
    users.child(user_id).set({"username": json["username"],
                              "active_room": room_id,
                              "created": datetime.datetime.now().day})

    # Send redirect information back to front-end
    emit('redirect', {'url': url_for("game", id=room_id),
                      'username': json["username"],
                      'userid': user_id})


if __name__ == "__main__":
    socketio.run(app, debug=True)
