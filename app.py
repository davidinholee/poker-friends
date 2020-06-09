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


# Main login page
@app.route("/")
def index():
    return render_template("index.html",
                           font_url1="https://fonts.googleapis.com/css?family=Amaranth",
                           font_url2="https://fonts.googleapis.com/css?family=Averia Libre",
                           socket_url="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.3/socket.io.js")


# Game page
@app.route('/<id>')
def game(id):
    return render_template("game.html",
                           font_url1="https://fonts.googleapis.com/css?family=Amaranth",
                           font_url2="https://fonts.googleapis.com/css?family=Averia Libre",
                           socket_url="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.3/socket.io.js",
                           room_id=id)


# Message printing
@socketio.on("message")
def handle_message(msg):
    print("Message:", msg)


# Joining a game room from the main page
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


# Creating a room from the main page
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
                if user_data[key]["active_room"] not in room_data:
                    users.child(key).delete()

    # Create unique user id
    user_id = str(uuid.uuid1())

    # Update database with new information
    rooms.child(room_id).set({"time_limit": json["time"],
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


# Making a user from the game page
@socketio.on('make-user')
def make_user(json):
    # Create unique user id
    user_id = str(uuid.uuid1())

    users.child(user_id).set({"username": json["username"],
                              "created": datetime.datetime.now().day,
                              "active_room": json["room_id"]})
    emit('set-cookies', {'username': json["username"], 'userid': user_id})


# Initial game page set up
@socketio.on('set-room')
def set_room(json):
    # Check if room still exists
    if rooms.child(json["room_id"]).child("created").get() is None:
        emit('redirect', {'url': url_for("index")})

    join_room(json["room_id"])
    room = rooms.child(json["room_id"])
    in_game = False
    new_user = True
    player_info = {}
    seat_num = -1
    # Check if account has been made for this room
    if json["room_id"] == users.child(json["user_id"]).child("active_room").get():
        new_user = False

    # Get all the players at the table's information
    user_list = room.child("users").get()
    if user_list is not None:
        for s in user_list:
            broken = False
            if s is None:
                s = 1
                broken = True
            p_id = user_list[s]
            if json["user_id"] == p_id:
                in_game = True
                seat_num = s
            p_username = users.child(p_id).child("username").get()
            p_chips = users.child(p_id).child("chips").get()
            player_info[s] = [p_username, p_chips]
            if broken:
                break

    # Check if game started
    started = rooms.child(json["room_id"]).child("started").get()
    if started is None:
        started = "no"

    emit("initialize-room", {'buy_in': room.child("buy_in").get(),
                             'small': room.child("small").get(),
                             'big': room.child("big").get(),
                             'new_user': new_user,
                             'in_game': in_game,
                             'seat': seat_num,
                             'players': player_info,
                             'started': started})


# Sitting down at the table
@socketio.on('sit-down')
def sit_down(json):
    rooms.child(json["room_id"]).child("users").child(json["seat"]).set(json["user_id"])
    users.child(json["user_id"]).child("chips").set(json["buy_in"])
    # Check if game started
    started = rooms.child(json["room_id"]).child("started").get()
    if started is None:
        started = "no"
    emit("new-player", {'seat': json["seat"],
                        'chips': json["buy_in"],
                        'username': json["username"],
                        'started': started}, room=json["room_id"])
    # Check if game should be started
    start = rooms.child(json["room_id"]).child("started").get()
    if (start is not None) and (start == "waiting"):
        start_game(json)

# Starting the game
@socketio.on('start-game')
def start_game(json):
    user_list = rooms.child(json["room_id"]).child("users").get()
    seats = list(user_list.keys())
    print(seats)
    # Set dealer
    dealer = -1
    for seat, user in user_list.items():
        if user == json["user_id"]:
            rooms.child(json["room_id"]).child("dealer").set(seat)
            dealer = seat

    if len(user_list) < 2:
        rooms.child(json["room_id"]).child("started").set("waiting")
        emit("enough-players", {'not_enough': True}, room=json["room_id"])
    else:
        rooms.child(json["room_id"]).child("started").set("started")
        emit("enough-players", {'not_enough': False}, room=json["room_id"])
        dealer = seats[seats.index(dealer) - 1]




if __name__ == "__main__":
    socketio.run(app, debug=True)
