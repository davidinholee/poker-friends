from flask import Flask, render_template, url_for, request, make_response, redirect
from flask_socketio import SocketIO, send, emit, join_room, leave_room
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
                           socket_url="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.3/socket.io.js")


@app.route('/<id>')
def game(id):
    return render_template("game.html",
                           font_url1="https://fonts.googleapis.com/css?family=Amaranth",
                           font_url2="https://fonts.googleapis.com/css?family=Averia Libre",
                           socket_url="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.3/socket.io.js",
                           room_id=id)


@socketio.on("message")
def handle_message(msg):
    print("Message:", msg)


@socketio.on('join-a-room')
def join_a_room(json):
    room_data = rooms.child(json["room_id"]).child("created").get()

    # Check that the room exists
    if room_data is not None:
        # Create unique user id
        user_id = str(uuid.uuid1())

        users.child(user_id).set({"username": json["username"],
                                          "active_room": json["room_id"],
                                          "created": datetime.datetime.now().day})

        # Send redirect information back to front-end
        emit('redirect', {'url': url_for("game", id=json["room_id"]),
                          'username': json["username"],
                          'userid': user_id})
    else:
        # Room doesn't exist
        emit('error')



@socketio.on('create-room')
def create_room(json):
    # Create unique room id.
    alphnum = string.ascii_lowercase + string.digits
    room_id = ''.join((random.choice(alphnum) for i in range(6)))
    room_data = rooms.child(room_id).child("created").get()
    i = 0
    while True:
        if room_data is None:
            break
        elif i > 1000:
            # If somehow not enough unique room ids, just return back to login
            emit('error2')
            return
        room_id = ''.join((random.choice(alphnum) for i in range(6)))
        room_data = rooms.child(room_id).child("created").get()
        i += 1

    room_data = rooms.get()
    user_data = users.get()
    day = int(datetime.datetime.now().day)
    # Clean up rooms database.
    if room_data is not None:
        for key in room_data:
            created = int(room_data[key]["created"])
            if (created + 1 < day) or (created >= 28 and day > 1 and day < 28):
                if "users" not in room_data[key]:
                    rooms.child(key).delete()

    if user_data is not None:
        # Clean up users database.
        for key in user_data:
            created = int(user_data[key]["created"])
            if (created + 1 < day) or (created >= 28 and day > 1 and day < 28):
                if user_data[key]["active_room"] not in room_data:
                    users.child(key).delete()

    # Create unique user id
    user_id = str(uuid.uuid1())

    # Update database with new information
    rooms.child(room_id).set({"users": [],
                              "time_limit": json["time"],
                              "small": json["small"],
                              "big": json["big"],
                              "buy_in": json["buy"],
                              "created": datetime.datetime.now().day})
    users.child(user_id).set({"username": json["username"],
                              "created": datetime.datetime.now().day,
                              "active_room": room_id})

    # Send redirect information back to front-end
    emit('redirect', {'url': url_for("game", id=room_id),
                      'username': json["username"],
                      'userid': user_id})


@socketio.on('make-user')
def make_user(json):
    # Create unique user id
    user_id = str(uuid.uuid1())

    users.child(user_id).set({"username": json["username"],
                              "created": datetime.datetime.now().day,
                              "active_room": json["room_id"]})
    emit('set-cookies', {'username': json["username"], 'userid': user_id})


@socketio.on('set-room')
def set_room(json):
    join_room(json["room_id"])
    room = rooms.child(json["room_id"])

    # Check if account has been made for this room
    new_user = True
    if json["room_id"] == users.child(json["user_id"]).child("active_room").get():
        new_user = False

    emit("initialize-room", {'buy_in': room.child("buy_in").get(),
                             'small': room.child("small").get(),
                             'big': room.child("big").get(),
                             'new_user': new_user})


if __name__ == "__main__":
    socketio.run(app, debug=True)
