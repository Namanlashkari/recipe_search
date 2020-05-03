from pymongo import MongoClient
from datetime import datetime
from elasticsearch import Elasticsearch
from flask import Flask, request
import re

mongo_username = 'add username here'
mongo_password = 'add password here'
#mongodb connection setup
mongouri = "mongodb+srv://"+mongo_username+":"+mongo_password+"@cluster0-dv5i4.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(mongouri)
db = client.Pakalo
collection = db.Recipes

app = Flask(__name__)

@app.route('/')
def hello():
    return ('please redirect your calls to 127.0.0.1:5000/ingredients')

@app.route('/test/')
def index():
    dict_obj = {
        'left': 0.17037454, 
        'right': 0.82339555, 
        '_unknown_': 0.0059609693
    }
    message = {
        'status': 200,
        'message': 'OK',
        'scores': dict_obj
    }
    resp = jsonify(message)
    resp.status_code = 200
    print(resp)
    return resp
@app.route('/ingredients/')
def ingredients():
    arg1 = request.args['arg1']
    params = arg1.split()
    for i in range(len(params)):
        params[i] = params[i].replace('_', ' ')
    #returns me all the document which contains the queried ingredients
    cursor = collection.find({ "ingredients": {"$in": params } })

    #all_recipes is a list of dictionary
    all_recipes = list(cursor)
    recipes_to_make = []

    for recipes in all_recipes:
        #total_ingredients is the total number of ingredients required to make the recipe
        total_ingredients = len(recipes["ingredients"])
        #this is the count of ingredients which the user has, to make the recipe
        avail_ingredients = 0
        for items in recipes["ingredients"]:
            if items in params:
                avail_ingredients += 1
        if total_ingredients == avail_ingredients:
            recipes_to_make.append(recipes["recipe_name"])

    json_response = {}
    all_response = {}
   
    for i in range(len(recipes_to_make)):
        recipe_name = recipes_to_make[i]
        picture_link = ""
        
        for items in all_recipes:
            if items['recipe_name'] == recipe_name:
                picture_link = items["picture_link"]
                print("picture_link and recipe_name %s %s" %(picture_link, recipe_name))    
                all_response['recipe_name']= recipe_name
                all_response['picture_link']=picture_link
        json_response.update(all_response)
        #all_response[i]["recipe_name"] = r_name
        #all_response[i]["picture_link"] = picture_link
        #print("\n values inside dictionary are " )
        #for ele in all_response:
            #print(ele)
        #print()
    print("json_response %s" %json_response)
    
    return json_response
