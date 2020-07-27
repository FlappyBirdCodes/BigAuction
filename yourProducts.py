from flask import Flask, render_template, request, redirect, session, flash, Blueprint
from pymongo import MongoClient
import pymongo
from urllib.request import urlopen
from helperFunctions import *
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products

your_product = Blueprint("your_product", __name__)

@your_product.route("/sell/<id>")
def sell(id):
    notificationsCount = notficationsCount(id)
    return render_template("sell.html", id=id, count=notificationsCount)

@your_product.route("/yourProducts/<id>")
def yourProducts(id):

    # Gets all products with userID
    all_products = Products.find({"usernameID": ObjectId(id)})

    allProducts_count = all_products.count()
    products = []

    for i in range(allProducts_count):
        product = all_products[i]

        # Defines product data
        product_data = {
            "id": i,
            "productID": product["_id"],
            "name": product["name"],
            "price": product["price"],
            "stock": product["amount"],
            "description": product["description"][:82],
            "image": product["url"]
        }

        products.append(product_data)

    notificationsCount = notficationsCount(id)

    return render_template("yourProducts.html", products=products, id=id, count=notificationsCount)

@your_product.route("/addProduct/<userID>", methods=["POST"])
def addProduct(userID):

    # Defines item data for user
    newProduct = {
        "usernameID": ObjectId(userID),
        "name": request.form.get("productName"),
        "price": request.form.get("price"),
        "amount": request.form.get("stockAmount"),
        "category": request.form.get("category"),
        "url": request.form.get("url"),
        "description": request.form.get("description")
    }

    #Changes url if user inputed url is not a real image
    if realImage(request.form.get("url")) is not True:
        newProduct["url"] = "https://www.freeiconspng.com/uploads/no-image-icon-11.PNG"

    # Adds new product to products collection
    Products.insert_one(newProduct)

    return redirect("/yourProducts/" + userID)

@your_product.route("/deleteProduct/<int:id>/<userID>", methods=["POST"])
def deleteProduct(id, userID):

    # Gets product that needs to be deleted
    all_products = Products.find({"usernameID": ObjectId(userID)})
    deleteProduct = all_products[id]

    Products.delete_one(deleteProduct)

    return redirect("/yourProducts/" + userID)







