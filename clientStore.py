from flask import Flask, render_template, request, redirect, session, flash, Blueprint
from pymongo import MongoClient
import pymongo
from helperFunctions import *

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products

clientStore = Blueprint("clientStore", __name__)

@clientStore.route("/store/<category>/<id>")
def store(category, id):

    if category == "all":
        products = Products.find({})
    else:
        products = Products.find({"category": category})
    products = list(products)

    sortRequest = request.args.get("sort")
    #Checks if sort request has been made
    if sortRequest:
        
        #Resorts product 
        products = sortProducts(sortRequest, products)

    #Determines which products to show depending on which page the user is on
    pageID = request.args.get("pageID")
    products = getProducts(products, pageID)[0]
    higherIndex = getProducts(products, pageID)[1]

    #Changes the footer colours 
    footerColours = changeFooterColours(higherIndex)    

    if id != "viewOnly":
        notificationsCount = notficationsCount(id)

    if category == "all":
        if id == "viewOnly":
            return render_template("viewStore.html", category="All Items", products=products, colours=footerColours, id=id)
        return render_template("store.html", category="All Items", products=products, colours=footerColours, id=id, count=notificationsCount)
    else:
        if id == "viewOnly":
            return render_template("viewStore.html", category=category, products=products, colours=footerColours, id=id)
        return render_template("store.html", category=category, products=products, colours=footerColours, id=id, count=notificationsCount)
