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

"""
import random
import string

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

@user_admission.route("/makeUsers", methods=["GET", "POST"])
def makeUsers():
    for i in range(1000):

        usernameLength = random.randint(8, 14)
        passwordLength = random.randint(14, 20)
        username = randomString(usernameLength)
        password = "patrickpatterson333"
        encoded_password = password.encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(encoded_password, salt)

        newUser = {
            "username": username,
            "password": hashed_password,
        }

        Users.insert_one(newUser)
    return redirect("/login")

def getUserID():
    users = Users.find({})
    users_count = users.count()
    userIndex = random.randint(0, users_count-1)
    userID = users[userIndex]["_id"]
    return userID

@user_admission.route("/makeProducts", methods=["GET", "POST"])
def makeProducts():
    
    for i in range(1000):
        categories = ["Baby", "Beauty", "Books", "Camera & Photo", "Clothing & Accessories", "Consumer Electronics", "Grocery & Gourmet Foods", "Health & Personal Care", 
            "Home & Garden", "Industrial & Scientific (BISS)", "Luggage & Travel Accessories", "Musical Instruments", "Office Products", "Outdoors", "Personal Computers",
            "Pet Supplies", "Shoes, Handbags & Sunglasses", "Software", "Sports", "Tools & Home Improvement", "Toys", "Video Games"]

        newProduct = {
            "usernameID": getUserID(),
            "name": randomString(12),
            "price": "$" + str(random.randint(1, 50)),
            "amount": random.randint(1, 100),
            "category": categories[random.randint(0, len(categories) - 1)],
            "url": urls[random.randint(0, len(urls) - 1)],
            "description": randomString(800).lower()
        }

        Products.insert_one(newProduct)

    return "testing"

@user_admission.route("/deleteProducts")
def deleteProducts():
    all_products = Products.find({})

    for product in all_products:
        Products.delete_one(product)

    return "done"

@user_admission.route("/deleteUsers")
def deleteUsers():
    all_users = Users.find({})

    for user in all_users:
        Users.delete_one(user)

    return "done"
"""