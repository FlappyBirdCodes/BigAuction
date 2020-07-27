from flask import Flask, render_template, request, redirect, session, flash, Blueprint
from pymongo import MongoClient
import pymongo
import random
from bson.objectid import ObjectId
from helperFunctions import * 

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products

Item = Blueprint("Item", __name__)

@Item.route("/item/<productID>/<userID>")
def item(productID, userID):
    
    #Find product from id
    product = Products.find_one({"_id": ObjectId(productID)})

    recommendedProducts = getRecommendedProducts(product["category"])
    firstProducts = recommendedProducts[0]
    secondProducts = recommendedProducts[1]

    return render_template("item.html", id=product["_id"], name=product["name"], category=product["category"], price=product["price"], amount=product["amount"], url=product["url"], description=product["description"], products1=firstProducts, products2=secondProducts, userId=userID)

@Item.route("/item/<productID>/viewOnly")
def viewOnlyItem(productID):

    #Find product from id
    product = Products.find_one({"_id": ObjectId(productID)})

    recommendedProducts = getRecommendedProducts(product["category"])
    firstProducts = recommendedProducts[0]
    secondProducts = recommendedProducts[1]

    return render_template("viewItem.html", id=product["_id"], name=product["name"], category=product["category"], price=product["price"], amount=product["amount"], url=product["url"], description=product["description"], products1=firstProducts, products2=secondProducts)
