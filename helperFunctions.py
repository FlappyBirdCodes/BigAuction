from flask import session
from urllib.request import urlopen
import validators
from pymongo import MongoClient
import pymongo
import random
from more_itertools import sort_together
from datetime import timedelta, datetime
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://flappybird:patrickpatterson333@bigauctionusers-o6oag.mongodb.net/<dbname>?retryWrites=true&w=majority")
Users = client.BigAuction.Users
Products = client.BigAuction.Products
Messages = client.BigAuction.Messages

#Checks if url is a real image
def realImage(url):
    if validators.url(url):
        image_formats = ("image/png", "image/jpeg", "image/gif")
        site = urlopen(url)
        meta = site.info() 
        if meta["content-type"] in image_formats:
            return True
        return False
    return False

#Returns recommended products for the user
def getRecommendedProducts(category=None):

    #Gets similar products
    if category is not None:
        similarProducts = Products.find({"category": category})
    else:
        similarProducts = Products.find({})

    similarProducts = list(similarProducts)

    recommendedProducts = []
    for i in range(12):
        randomIndex = random.randint(0, len(similarProducts) - 1)
        similarProduct = similarProducts[randomIndex]
        product_data = {
            "id": similarProduct["_id"],
            "url": similarProduct["url"]
        }
        recommendedProducts.append(product_data)
        similarProducts.remove(similarProduct)

    firstProducts = recommendedProducts[:4]
    secondProducts = recommendedProducts[4:8]    
    thirdProducts = recommendedProducts[8:]

    return firstProducts, secondProducts, thirdProducts

def sortProducts(sortRequest, products):

    print(products)
    #Sorts by price
    if sortRequest == "sortByPrice":        
        products.sort(key=lambda  product: float(product["price"][1:]))

    #Sorts by stock amount
    elif sortRequest == "sortByStock":
        products.sort(key=lambda  product: int(product["amount"]), reverse=True)
    return products

def getProducts(products, pageID):
    if pageID == None:
        lowerIndex = 0
        higherIndex = 27
    else:
        lowerIndex = 27 * int(pageID)
        higherIndex = 27 * (1 + int(pageID)) 
    return products[lowerIndex:higherIndex], higherIndex

def changeFooterColours(higherIndex):
    footerColours = [[1, "secondary"], [2, "secondary"], [3, "secondary"], [4, "secondary"], [5, "secondary"], [6, "secondary"], [7, "secondary"], [8, "secondary"], [9, "secondary"], [10, "secondary"], [11, "secondary"], [12, "secondary"]]
    currentIndex = int(higherIndex / 27 - 1)
    footerColours[currentIndex][1] = "success"
    return footerColours

def getMonth(month):
    months = [
        "January", "Febuary", "March",
        "April", "May", "June", "July",
        "August", "September", "October",
        "November", "December"
    ]
    return months[month - 1]

def getEnding(date):
    endingLetter = int(date[-1])
    endings = [
        "th", "st", "nd", "rd",
        "th", "th", "th",
        "th", "th", "th", 
    ]
    return str(endingLetter) + endings[endingLetter]

def oneWeekDate():
    from datetime import date
    new_date = (date.today()+timedelta(days=7)).isoformat()
    new_date = new_date.split("-")

    year = new_date[0]
    month = int(new_date[1])
    date = new_date[2]

    month = getMonth(month)
    date = getEnding(date)
    finalString = month + " " + date + ", " + year
    return finalString

def notficationsCount(id):
    notifications = list(Messages.find({"inbox": ObjectId(id)}))
    return len(notifications)
