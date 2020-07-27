from flask import Flask, render_template, request, redirect, session, flash, Blueprint
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
from helperFunctions import *
import time

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products
Cart = client.BigAuction.Cart

cart = Blueprint("cart", __name__)

@cart.route("/yourCart/<id>")
def yourCart(id):

    products = Cart.find({"usernameID": ObjectId(id)})
    products = list(products)

    for product in products:
        product["product"] = "/item/" + str(product["productID"]) + "/" + id
        product["categoryLink"] = "/store/" + product["category"] + "/" + id

    notificationsCount = notficationsCount(id)

    return render_template("cart.html", products=products, id=id, count=notificationsCount)

#Adds product to cart
@cart.route("/addToCart/<id>/<userID>", methods=["POST"])
def addToCart(id, userID):

    # Gets product information
    productID = ObjectId(id)
    product = Products.find_one({"_id": productID})
    
    # Gets user data
    user = Users.find_one({"_id": ObjectId(userID)})

    #Gets quantity request and actual quantity of product
    quantity = int(request.form.get("quantity"))
    productQuantity = int(product["amount"])

    #Checks if user is buying their own product
    if product["usernameID"] == ObjectId(userID):
        flash("You cannot buy your own product.")
        return redirect("/item/" + id + "/" + userID)

    if quantity <= productQuantity:
        cartProduct = {
            "usernameID": ObjectId(userID),
            "productID": productID,
            "url": product["url"],
            "name": product["name"],
            "category": product["category"],
            "quantity": quantity,
            "price": product["price"]
        }

        #Deletes amount from product, will add back to product if user chooses not buy
        remainingQuantity = productQuantity - quantity
        addedProduct = Products.find_one_and_update(
            {"_id": productID},
            {"$set":
                {"amount": remainingQuantity}
            }, upsert=True
        )

        # Adds new product to cart collection
        Cart.insert_one(cartProduct)

        return redirect("/yourCart/" + userID)
    return "not enough in stock"

#Deletes product from cart
@cart.route("/deleteFromCart/<id>/<quantity>/<userID>", methods=["POST"])
def deleteFromCart(id, quantity, userID):

    #Finds product with the same id
    product = Cart.find_one({"_id": ObjectId(id)})

    #Adds product quantity back to original product
    productID = product["productID"]
    addQuantity = Products.update_one(
        {"_id": productID},
        {"$inc": {"amount": int(quantity)}
        }, upsert=True    
    )

    Cart.delete_one(product)

    return redirect("/yourCart/" + userID)






