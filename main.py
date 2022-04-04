from flask import Flask, render_template, request, json, jsonify
import random
import time

import base64  # imgkit
import os  # imgkit
import sys  # imgkit
from imagekitio import ImageKit  # imgkit

app = Flask(__name__)


def read_restaurant_data():
  with open("static/data/restaurant.json") as file:
    data = json.load(file)
  return data


def write_restaurant_data(data):
  with open("static/data/restaurant.json", mode="w") as f:
    json.dump(data, f)


def reflashImagekitKey():  # kitimage get private_key
  imagekit = ImageKit(
      public_key='public_4YpxagNybX9kAXW6yNx8x9XnFX0=',
      private_key='private_S9iytnyLQd+abJCWH7H/iwygXHc=',
      url_endpoint='https://ik.imagekit.io/csiejarimgstorage'
  )
  auth_params = imagekit.get_authentication_parameters()
  return auth_params


def check_restaurant_amount():  # reload restaurant amount

  data = read_restaurant_data()
  amount = len(data["restaurant_list"])
  data["restaurant_amount"] = amount
  write_restaurant_data(data)

def check_accepted_list():
  data = read_restaurant_data()
  data["restaurant_names_accepted"].clear()
  for i in data["restaurant_list"]:
    if i["accept"] == "true":
      data["restaurant_names_accepted"] = i["id"]



@app.route('/')
def index_page():  # home page html
  check_restaurant_amount()
  check_accepted_list()
  return render_template("home.html")


@app.route('/random', methods=["POST"])
def random_restaurant():  # get random data
  data = read_restaurant_data()
  restaurant_amount = data["restaurant_amount"]
  random_index = random.randint(0, restaurant_amount-1)
  random_name = data["restaurant_names"][random_index]
  output_data = data["restaurant_list"][random_name]

  return jsonify(output_data)


@app.route('/add_restaurant', methods=["GET"])
def edit_page():  # edit page html
  return render_template("edit.html")


@app.route('/edit_data', methods=["GET", "POST", "PUT", "DELETE"])
def add_data():  # add restaurant data
  if request.method == "POST":

    data = read_restaurant_data()
    num = data["restaurant_amount"]
    uuidstr = uuid.uuid4()
    data["restaurant_list"][uuidstr]={
            "content": {
                "restaurant_num": "0"*(3-(len(str(num+1))))+str(num+1),
                "restaurant_title": request.form["restaurant_title"],
                "restaurant_img_url": request.form["restaurant_img_url"],
                "menu_img_url": request.form["menu_img_url"],
                "menu_text": request.form["menu_text"],
                "prefer_dish_img_url": request.form["prefer_dish_img_url"],
                "prefer_dish_text": request.form["prefer_dish_text"],
                "restaurant_googlemap_link": request.form["restaurant_googlemap_link"],
            },
            "id":uuidstr,
            "creat_time": time.ctime(time.time()+28800),
            "accept": "false",
            "creator": ""

        }

        
    
    data["restaurant_amount"] += 1
    write_restaurant_data(data)
    return jsonify({"messenge": "up load success"})
  elif request.method == "PUT":
    put_data_mode = request.form.get("put_data_mode")
    data_num = request.form.get("data_num")
    if put_data_mode == "content":
      print("edit content")
    elif put_data_mode == "header":
      print("header")
      data = read_restaurant_data()
      change_data = request.form.get("accept")
      # print(type(change_data))
      data["restaurant_list"][data_num]["accept"] = change_data
      # print(data["restaurant_list"][data_num])
      write_restaurant_data(data)
      return jsonify({"messenge": "change header success"})

    else:
      print("no type")
  elif request.method == "DELETE":
    data_num = request.form.get("data_num")
    data = read_restaurant_data()
    del data["restaurant_list"][data_num]
    data["restaurant_names"].remove(data_num)
    # print(data_num)
    write_restaurant_data(data)
    return jsonify({"messenge": "del success"})
  elif request.method == "GET":
    data_num = request.form.get("data_num")

    data = read_restaurant_data()
    output = data["restaurant_list"][data_num]
    return jsonify(output)


@app.route('/uploadImage')
def returnPrivateKay():  # response private_key
  return jsonify(reflashImagekitKey())


@app.route("/login")
def login():  # login page
  return render_template("login.html")


@app.route("/demo_page", methods=['GET', "POST"])
def target_page():  # get demo html and demo data
  if request.method == "GET":
    output = request.args.get("data_num")
    return render_template("demo.html", get_data_num=output)
  elif request.method == "POST":
    data_num = request.form.get("data_num")

    try:
      data = read_restaurant_data()
      output = data["restaurant_list"][data_num]
      output["status"] = "true"
      return jsonify(output)
    except Exception:
      return jsonify({"status":"false"})



@app.route("/get_restaurant_amount")
def get_restaurant_amount():  # get restaurant data
  data = read_restaurant_data()
  return jsonify({"restaurant_amount": data["restaurant_amount"],"restaurant_names": data["restaurant_names"]})


#run server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
