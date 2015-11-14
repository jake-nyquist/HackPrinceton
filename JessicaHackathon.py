from flask import Flask
from flask import request
from pymongo import MongoClient
import json
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("jessmongodb.cloudapp.net", 27017)
db = client.Princeton
collection = db["events"]

@app.route('/')
def hello_world():
    return 'Hi World!'

@app.route('/addevent', methods=['POST'])
def add_event():
    event = {
        "name": request.form["name"],
        "location": request.form["location"],
        #"time": request.form["time"]
    }
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
        return str(json.dumps(details))
    except:
        return "{}"


@app.route('/upvote/<int:eventID>')
def upvote(eventID):
    return 'upvote: ' + str(eventID)

@app.route('/findevents/')
def find_events():
    return 'upvote: ' + str()

@app.route('/report/<int:eventID>')
def report(eventID):
    return 'report: ' + str(eventID)

if __name__ == '__main__':
    app.run()
