from flask import Flask, render_template, request, redirect, session, flash, Blueprint
from pymongo import MongoClient
import pymongo
import bcrypt

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products

user_admission = Blueprint("user_admission", __name__)

@user_admission.route("/login", methods=["GET", "POST"])
def login():
    
    # Renders login page
    if request.method == "GET":
        return render_template("login.html")

    # When user logs into their account
    else:

        # Data submitted from log in form
        username = request.form.get("username")
        password = request.form.get("password")

        # Looks for username
        user = Users.find_one({"username": username})

        # Checks if username exists
        if user:

            # Sets session variable
            session["username"] = user["username"]

            # Checks if entered password matches actual password
            actual_password = user["password"]
            encoded_password = password.encode()
            if bcrypt.hashpw(encoded_password, actual_password) == actual_password:
                return redirect("/homepage/" + str(user["_id"]))

            else:
                flash("Your password is incorrect.")
                return redirect("/login")

        else:
            flash("This username doesn't exist.")
            return redirect("/login")


@user_admission.route("/signup", methods=["GET", "POST"])
def signup():
    # Renders sign up page
    if request.method == "GET":
        return render_template("signup.html")

    # When user makes a new account
    else:

        # Data submitted from sign up form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")

        #Checks for other users with the same username
        userWithSameUsername = list(Users.find({"username": username}))
        if len(userWithSameUsername) > 0:
            flash("This username already exists. Please try again.")
            return redirect("/signup")

        # Checks that password and confirm password are the same
        if password == confirmPassword:

            # Generates hashed password
            encoded_password = password.encode()
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(encoded_password, salt)

            # Defines data for new user
            newUser = {
                "username": username,
                "password": hashed_password,
            }

            Users.insert_one(newUser)
            return redirect("/login")

        else:
            flash("Password and confirm password must be the same.")
            return redirect("/signup")
