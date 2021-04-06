import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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
    recipies = list(mongo.db.recipies.find())
    return render_template("recipies.html", recipies=recipies)


@app.route("/register", methods=["GET", "POST"])
def register():
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
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            #if statement shows line too long error, but if fixed, shows indentation error instead
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
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/find")
def find():
    return render_template("find.html")


@app.route("/add", methods=["GET", "POST"])
def add():
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
    return render_template("add.html", categories=categories)


@app.route("/edit_recipie/<recipie_id>", methods=["GET", "POST"])
def edit_recipie(recipie_id):
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
    return render_template("edit_recipie.html", recipie=recipie, categories=categories)


@app.route("/delete_recipie/<recipie_id>")
def delete_recipie(recipie_id):
    mongo.db.recipies.remove({"_id": ObjectId(recipie_id)})
    return redirect(url_for("get_recipies"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
