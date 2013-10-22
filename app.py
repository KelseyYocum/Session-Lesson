from flask import Flask, render_template, request, redirect, session, url_for, flash, g
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"


@app.before_request
def before_request():
    g.db = model.connect_to_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    if session.get("username"):
        return "User %s is logged in!" %session['username']
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")

    user_id = model.authenticate(username, password)
    if user_id != None:
        flash("User authenticated!")
        session['id'] = user_id
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")
    return redirect(url_for ("view_user", username = username))

@app.route("/clear")
def clear_session():
    session.clear()
    return redirect(url_for ("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/user/<username>")
def view_user(username):

    wall_posts = model.wall_posts(username)
    return render_template("wall.html", wall_posts = wall_posts, username = username, user_id =session.get('id', None))

if __name__ == "__main__":
    app.run(debug = True)
