from flask import Flask, render_template, request, json, jsonify
import random
import time

import base64#imgkit
import os#imgkit
import sys#imgkit
from imagekitio import ImageKit#imgkit


def reflashImagekitKey():
  imagekit = ImageKit(
      public_key='public_4YpxagNybX9kAXW6yNx8x9XnFX0=',
      private_key='private_S9iytnyLQd+abJCWH7H/iwygXHc=',
      url_endpoint = 'https://ik.imagekit.io/csiejarimgstorage'
  )
  auth_params = imagekit.get_authentication_parameters()
  return auth_params
  


app = Flask(__name__)

def check_restaurant_amount():
  with open("static/data/restaurant.json") as f:
    data = json.load(f)
  amount = len(data["restaurant_list"])
  data["restaurant_amount"] = amount
  with open("static/data/restaurant.json",mode="w") as f:
    json.dump(data,f)
    
@app.route('/')
def index_page():
  check_restaurant_amount()
  return render_template("home.html")

@app.route('/random',methods=["POST"])
def random_restaurant():
  with open("static/data/restaurant.json") as f:
    data = json.load(f)
  restaurant_amount = data["restaurant_amount"]
  random_index = random.randint(0,restaurant_amount-1)
  output_data = data["restaurant_list"][random_index]
  
  return jsonify(output_data)
@app.route('/add_restaurant',methods=["GET"])
def edit_page():
  return render_template("edit.html")

@app.route('/add',methods=["POST"])
def add_data():
  with open("static/data/restaurant.json") as f:
    data = json.load(f)
  num = data["restaurant_amount"]
  data["restaurant_list"].append(
    {
      "restaurant_num":"0"*(3-(len(str(num+1))))+str(num+1),
      "restaurant_title": request.form["restaurant_title"],
      "restaurant_img_url": request.form["restaurant_img_url"],
      "menu_img_url": request.form["menu_img_url"],
      "menu_text": request.form["menu_text"],
      "prefer_dish_img_url": request.form["prefer_dish_img_url"],
      "prefer_dish_text": request.form["prefer_dish_text"],
      "restaurant_googlemap_link": request.form["restaurant_googlemap_link"],
      "creat_time":time.ctime(time.time()+28800),
      "accept":False,
      "creator":""
    }
  )
  data["restaurant_amount"] += 1
  with open("static/data/restaurant.json",mode="w") as f:
    json.dump(data, f)
  return jsonify({"messenge":"up load sucess"})

@app.route('/uploadImage')
def returnPrivateKay():
  return jsonify(reflashImagekitKey())
@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/demo_page",methods=['GET',"POST"])
def target_page():
  if request.method == "GET":
    output = request.args.get("data_num")
    return render_template("demo.html",get_data_num=output)
  elif request.method == "POST":
    print("asedfasdf")
    data_num = request.form.get("data_num")
    with open("static/data/restaurant.json") as f:
      data = json.load(f)
    output = data["restaurant_list"][int(data_num)]
    return jsonify(output)
  
@app.route("/get_restaurant_amount")
def get_restaurant_amount():
  with open("static/data/restaurant.json") as file:
    data = json.load(file)
  return jsonify({"restaurant_amount":data["restaurant_amount"]})
#run server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)