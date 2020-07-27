from flask import Flask, render_template, request, redirect, session, flash, Blueprint
from pymongo import MongoClient
import pymongo
import time
from helperFunctions import *
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products
Cart = client.BigAuction.Cart
Messages = client.BigAuction.Messages

userCheckout = Blueprint("userCheckout", __name__)

@userCheckout.route("/checkoutPage/<id>")
def checkoutPage(id):
    notificationsCount = notficationsCount(id)

    return render_template("checkoutPage.html", total=session["totalCost"], id=id, count=notificationsCount)

@userCheckout.route("/checkout/<userID>", methods=["POST"])
def checkout(userID):

    totalCost = 0

    #Finds total cost of all products in the cart
    cartProducts = Cart.find({"usernameID": ObjectId(userID)})
    for cartProduct in cartProducts:
        price = float(cartProduct["price"][1:])
        totalCost += price

    if totalCost > 0:
        session["totalCost"] = request.form.get("totalCost")
        return redirect("/checkoutPage/" + userID)
    flash("You have no items in your cart.")
    return redirect("/yourCart/" + userID)

#This route is broken. Needs to be fixed
@userCheckout.route("/success/<userID>", methods=["POST"])
def successPage(userID):

    cartProducts = list(Cart.find({"usernameID": ObjectId(userID)}))

    if len(cartProducts) > 0:

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        for i in range(len(cartProducts)):

            #Gets seller data
            seller = Products.find_one({"_id": cartProducts[i]["productID"]})
            sellerID = seller["usernameID"]

            message = {
                "inbox": sellerID,
                "buyer": ObjectId(userID),
                "seller": sellerID,
                "cartProducts": cartProducts[i],
                "time": current_time
            }

            Messages.insert_one(message)

        #Deletes all items from cart
        for cartProduct in cartProducts:
            Cart.delete_one(cartProduct)

        #Deletes all products with 0 quantity
        noQuantity = Products.find({"amount": 0})
        for product in noQuantity:
            Products.delete_one(product)

    notificationsCount = notficationsCount(userID)

    return render_template("success.html", id=userID, count=notificationsCount)






