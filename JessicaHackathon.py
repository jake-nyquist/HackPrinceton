from flask import Flask
from flask import request
from pymongo import MongoClient
import json
from dateutil import parser
from bson.objectid import ObjectId
from bson import timestamp
from dateutil import parser
parser.parse("Tue May 08 15:14:45 +0800 2012")
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
        return str(json.dumps(details))
    except:
        return "{}"


@app.route('/upvote/<int:eventID>')
def upvote(eventID):
    return 'upvote: ' + str(eventID)

@app.route('/report/<int:eventID>')
def report(eventID):
    return 'report: ' + str(eventID)

@app.route('/findevents/')
def find_events():
    return 'upvote: ' + str()



if __name__ == '__main__':
    app.run()
