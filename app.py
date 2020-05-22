from flask import Flask, render_template, url_for

# Create app with template and routes folders pointed to correct locations
app = Flask(__name__, template_folder="resources/templates/", static_folder="resources/static/")

@app.route("/")
def index():
    return render_template("index.html",
                           font_url1="https://fonts.googleapis.com/css?family=Amaranth",
                           font_url2="https://fonts.googleapis.com/css?family=Averia Libre")

if __name__ == "__main__":
    app.run(debug=True)
