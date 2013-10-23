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
        return redirect(url_for ("view_user", username = username))
    else:
        flash("Password incorrect, there may be a ferret stampede in progress!")
        return redirect(url_for("index"))

@app.route("/clear")
def clear_session():
    session.clear()
    return redirect(url_for ("index"))

@app.route("/register")
def register():
    if session.get('id', None) != None:
        user_id = (session['id'])
        username = model.given_id_return_name(user_id)
        return redirect(url_for("view_user", username=username))
    else:
        return render_template("register.html")

@app.route("/register", methods=["POST"])
def create_account():
    username = request.form.get("username")
    password = request.form.get("password")

    if model.given_name_return_id(username):
        flash("You already have an account!")
        return redirect(url_for("index"))
    else:
        model.create_account(username, password)
        flash ("You have successfully created an account!")
        return redirect(url_for("index"))

@app.route("/user/<username>")
def view_user(username):
    if model.given_name_return_id(username):
        wall_posts = model.wall_posts(username)
        return render_template("wall.html", wall_posts = wall_posts, username = username, user_id =session.get('id', None))
    else:
        flash("Sorry, this user is not registered yet.")
        return redirect(url_for("index"))    

#username of the wall's owner
@app.route("/user/<username>", methods=["POST"])
def post_to_wall(username):
    content = request.form.get('post')
    if content:
        author_id = session.get('id', None)
        model.add_wall_post(username, author_id, content)
        
    else:
        flash("Message field is empty!")

    return redirect(url_for("view_user", username = username))
if __name__ == "__main__":
    app.run(debug = True)
