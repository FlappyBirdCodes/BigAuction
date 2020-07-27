from flask import Flask, render_template, request, redirect, session, flash, Blueprint
from pymongo import MongoClient
import pymongo
from helperFunctions import *
from bson.objectid import ObjectId
import time

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products
Cart = client.BigAuction.Cart
Messages = client.BigAuction.Messages

userNotifications = Blueprint("userNotifications", __name__)

@userNotifications.route("/notifications/<id>")
def notifications(id):

    purchases = list(Messages.find({"inbox": ObjectId(id)}))

    allPurchaseData = []

    for purchase in purchases:
        #Gets buyers and sellers 
        buyer = Users.find_one({"_id": purchase["buyer"]})
        seller = Users.find_one({"_id": purchase["seller"]})

        product = purchase["cartProducts"]
        product["notificationId"] = purchase["_id"]
        product["buyer"] = buyer["username"]
        product["time"] = purchase["time"]
        cost = product["quantity"] * int(product["price"][1:])

        arrival_date = oneWeekDate()

        #Checks if it's a buying notification
        if purchase["seller"] == ObjectId(id):
            product["action"] = "shipped"
            product["label"] = "Shipped?"
            product["message"] = buyer["username"] + " has purchased " + str(product["quantity"]) + " " + product["name"] + " for $" + str(cost) + ". Please ship the product before " + arrival_date + " to avoid any penalties."

        #Checks if it's a recieving notification
        else:
            product["action"] = "expecting"
            product["label"] = "Got it?"
            product["message"] = seller["username"] + " is shipping your " + product["name"] + " to you. Expected arrival date is " + arrival_date + "."
        
        allPurchaseData.append(product)

    notificationsCount = notficationsCount(id)

    return render_template("notifications.html", notifications=allPurchaseData, id=id, count=notificationsCount)

@userNotifications.route("/shipped/<id>/<notificationId>", methods=["POST"])
def shipped(id, notificationId):

    message = Messages.find_one({"_id": ObjectId(notificationId)})
    cartProducts = message["cartProducts"]

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    newMessage = {
        "inbox": message["buyer"],
        "buyer": message["buyer"],
        "seller": ObjectId(id),
        "cartProducts": cartProducts,
        "time": current_time
    }

    Messages.delete_one(message)
    Messages.insert_one(newMessage)

    return redirect("/notifications/" + id)

@userNotifications.route("/expecting/<id>/<notificationId>", methods=["POST"])
def expecting(id, notificationId):

    message = Messages.find_one({"_id": ObjectId(notificationId)})
    Messages.delete_one(message)

    return redirect("/notifications/" + id)