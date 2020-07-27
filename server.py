from flask import Flask, render_template, request, redirect, session, flash
from pymongo import MongoClient
import pymongo
from yourProducts import your_product
from UserAdmission import user_admission
from clientStore import clientStore
from item import Item
from cart import cart
from search import searchEngine
from checkout import userCheckout
from notifications import userNotifications
import random
from helperFunctions import *
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "secret key"

app.register_blueprint(your_product)
app.register_blueprint(user_admission)
app.register_blueprint(clientStore)
app.register_blueprint(Item)
app.register_blueprint(cart)
app.register_blueprint(searchEngine)
app.register_blueprint(userCheckout)
app.register_blueprint(userNotifications)

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products

@app.route("/")
def home():

    #Randomly selects 3 different categories to display
    categories = ["Baby", "Beauty", "Books", "Camera & Photo", "Clothing & Accessories", "Consumer Electronics", "Grocery & Gourmet Foods", "Health & Personal Care", 
        "Home & Garden", "Industrial & Scientific (BISS)", "Luggage & Travel Accessories", "Musical Instruments", "Office Products", "Outdoors", "Personal Computers",
        "Pet Supplies", "Shoes, Handbags & Sunglasses", "Software", "Sports", "Tools & Home Improvement", "Toys", "Video Games"]
    category1 = random.choice(categories)
    categories.remove(category1)
    category2 = random.choice(categories)
    categories.remove(category2)
    category3 = random.choice(categories)

    newBestSellers = getRecommendedProducts()
    newProducts1 = getRecommendedProducts(category1)
    newProducts2 = getRecommendedProducts(category2)
    newProducts3 = getRecommendedProducts(category3)

    newBestSellers1 = newBestSellers[0]
    newBestSellers2 = newBestSellers[1]
    products1 = newProducts1[0]
    products2 = newProducts1[1]
    products3 = newProducts2[0]
    products4 = newProducts2[1]
    products5 = newProducts3[0]
    products6 = newProducts3[1]

    # Renders home page
    return render_template("index.html", category1=category1, category2=category2, category3=category3, newBestSellers1=newBestSellers1, newBestSellers2=newBestSellers2, products1=products1, products2=products2, products3=products3, products4=products4, products5=products5, products6=products6)

@app.route("/homepage/<id>")
def homepage(id):

    recommendedProducts = getRecommendedProducts()
    products1 = recommendedProducts[0]
    products2 = recommendedProducts[1]

    notificationsCount = notficationsCount(id)

    username = Users.find_one({"_id": ObjectId(id)})
    username = username["username"]
    if username:
        return render_template("homepage.html", username=username, products1=products1, products2=products2, id=id, count=notificationsCount)
    return "user does not exist"

if __name__ == "__main__":
    app.run(debug=True)












