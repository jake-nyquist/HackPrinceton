from flask import Flask
from flask import request, redirect, url_for, render_template
from pymongo import MongoClient, GEOSPHERE
import json
from dateutil import parser
from bson.objectid import ObjectId
from bson import timestamp
from bson.son import SON
from dateutil import parser
import time


parser.parse("Tue May 08 15:14:45 +0800 2012")
app = Flask(__name__)

client = MongoClient("jessmongodb.cloudapp.net", 27017)
db = client.Princeton
collection = db["events"]
collection.create_index([("location", GEOSPHERE)])

@app.route('/')
def hello_world():
    return redirect(url_for('static'), "index.html")

@app.route("/addeventform")
def event_form():
    return render_template("eventform.html")


@app.route('/addevent', methods=['POST'])
def add_event():
    event = {
    }
    lat= 0
    long = 0
    for i in request.form.keys():
        if i== "lat":
            lat = int(request.form[i])
        elif i== "long":
            long = int(request.form[i])
        elif i=="time":
            time = parser.parse(request.form[i])
            event["time"] = timestamp.Timestamp(time,0)
        else:
            event[i]= request.form[i]
    event["location"] = [lat,long]
    event["upvotes"] = 0
    event["visible"] = True
    try:
        post_id = collection.insert_one(event).inserted_id
    except:
        return "Exception"
    return 'This will eventually add an event' + str(post_id)

@app.route('/eventdetails/<eventID>')
def event_detail(eventID):
    try:
        details = collection.find_one({'_id': ObjectId(eventID)})
        details["_id"] = str(details["_id"])
        details["time"] = str(details["time"].as_datetime().isoformat())
        return render_template("eventdetails.html", det = details, flag = True)
    except:
        return render_template("eventdetails.html", det = None, flag = True)


@app.route('/upvote/<eventID>')
def upvote(eventID):
    result = collection.update_one({'_id': ObjectId(eventID)}, {"$inc": {"upvotes": 1}})
    return "{\"result\" : \"success\"}"

@app.route('/report/<eventID>')
def report(eventID):
    result = collection.update_one({'_id': ObjectId(eventID)}, {"$set": {"visible": False}})
    return 'report: ' + str(eventID)

@app.route('/findevents/')
@app.route('/findevents/<int:limit>', methods=["GET","POST"])
def find_events(limit = 10):
    # lat = float(request.form["lat"])
    # long = float(request.form["long"])
    # limit = int(request.form["limit"])
    results = collection.find().limit(limit)
    res = []
    for rest in results:
        print rest
        rest["_id"] = str(rest["_id"])
        rest["time"] = str(rest["time"].as_datetime().isoformat())
        res.append(rest)
    return render_template('index.html', rest = res)



if __name__ == '__main__':
    app.run()
