from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, send

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


@socketio.on("message")
def handle_message(msg):
    print("Message:", msg)


@socketio.on('create-room')
def create_room(json):
    print('received json: ' + str(json))


if __name__ == "__main__":
    socketio.run(app, debug=True)
