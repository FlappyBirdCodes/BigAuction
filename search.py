from flask import Flask, render_template, request, redirect, session, flash, Blueprint
from pymongo import MongoClient
import pymongo
from helperFunctions import *

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products

searchEngine = Blueprint("searchEngine", __name__)

@searchEngine.route("/search/<id>", methods=["POST"])
def search(id):
    search = request.form.get("search").lower()
    return redirect("/search/" + id + "/" + search)

@searchEngine.route("/search/<id>/<search>")
def formatSearch(id, search):

    results = []

    items = list(Products.find({}))
    for item in items:
        if search in item["name"].lower() or search in item["category"].lower() or search in item["description"].lower():
            results.append(item)

    sortRequest = request.args.get("sort")
    if sortRequest:
        
        #Resorts product 
        results = sortProducts(sortRequest, results)

    #Determines which products to show depending on which page the user is on
    pageID = request.args.get("pageID")
    results = getProducts(results, pageID)[0]
    higherIndex = getProducts(results, pageID)[1]

    #Changes the footer colours 
    footerColours = changeFooterColours(higherIndex)    

    if id != "viewOnly":
        notificationsCount = notficationsCount(id)

    if id == "viewOnly":
        return render_template("viewSearch.html", id=id, products=results, category="Search: " + search, colours=footerColours)
    return render_template("store.html", id=id, products=results, category="Search: " + search, colours=footerColours, count=notificationsCount)