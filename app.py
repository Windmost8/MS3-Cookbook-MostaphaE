import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_recipies")
def get_recipies():
    """
    This will fetch recipies created/pre included in the Mongo database and create a list to be shown on recipies.html
    """
    recipies = list(mongo.db.recipies.find())
    return render_template("recipies.html", recipies=recipies)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    This is the search bar functionality that will find from the mongo database
    """
    query = request.form.get("query")
    recipies = list(mongo.db.recipies.find({"$text": {"$search": query}}))
    return render_template("recipies.html", recipies=recipies)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    This will check user authentication and creation,
    whether a certain username/password exists in the mongo databse,
    and then finally adds them into the session cookie for the site.
    """
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Similiar to the register app above,
    this will check whether the form values are correct/found in the database
    in order to log in to the site.
    """
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                        request.form.get("username")))
                return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    A profile page that shows the current session user's username
    """
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    Logout functionality, popping the session user cookie.
    """
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/error")
def error():
    """
    An error page for redirection
    purposes at user authentication/anonymys users.
    """
    return render_template("error.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Creation of recipies updated into the mongo database from the site form.
    Also showcased on the site
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        if request.method == "POST":
            recipie = {
                "category_name": request.form.get("category_name"),
                "recipie_name": request.form.get("recipie_name"),
                "ingredients": request.form.get("ingredients"),
                "preparation": request.form.get("preparation"),
                "special_tools": request.form.get("special_tools"),
                "created_by": session["user"]
            }
            mongo.db.recipies.insert_one(recipie)
            flash("Recipie Added!")
            return redirect(url_for("get_recipies"))

        categories = mongo.db.categories.find().sort("category_name", 1)
        return render_template(
            "add.html", categories=categories, username=username
            )
    if not session["user"]:
        return redirect(url_for("error"))


@app.route("/edit_recipie/<recipie_id>", methods=["GET", "POST"])
def edit_recipie(recipie_id):
    """
    Edit functionality by user for existing recipies.
    This updates the mongo database
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        if request.method == "POST":
            submit = {
                "category_name": request.form.get("category_name"),
                "recipie_name": request.form.get("recipie_name"),
                "ingredients": request.form.get("ingredients"),
                "preparation": request.form.get("preparation"),
                "special_tools": request.form.get("special_tools"),
                "created_by": session["user"]
            }
            mongo.db.recipies.update({"_id": ObjectId(recipie_id)}, submit)
            flash("recipie Successfully Updated")

        recipie = mongo.db.recipies.find_one({"_id": ObjectId(recipie_id)})
        categories = mongo.db.categories.find().sort("category_name", 1)
        return render_template("edit_recipie.html", recipie=recipie, categories=categories, username=username)


@app.route("/delete_recipie/<recipie_id>")
def delete_recipie(recipie_id):
    """
    Delete functinoality, removing the recipie in question
    from the mongo database.
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        mongo.db.recipies.remove({"_id": ObjectId(recipie_id)})
        return redirect(url_for("get_recipies"))


@app.route("/get_categories")
def get_categories():
    """
    This fetches existing and created categories
    from the mongo database
    and showcases them on categories.html
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        categories = list(mongo.db.categories.find().sort("category_name", 1))
        return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """
    Add functionality to the categories
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        if request.method == "POST":
            category = {
                "category_name": request.form.get("category_name")
            }
            mongo.db.categories.insert_one(category)
            return redirect(url_for("get_categories"))

        return render_template("add_category.html")


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    """
    similar to the add functinality of categories
    but instead edit functionality
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        if request.method == "POST":
            submit = {
                "category_name": request.form.get("category_name")
            }
            mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
            return redirect(url_for("get_categories"))

        category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
        return render_template("edit_category.html", category=category)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    """
    Delete functinality for categories
    removing them from the database
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        mongo.db.categories.remove({"_id": ObjectId(category_id)})
        return redirect(url_for("get_categories"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
