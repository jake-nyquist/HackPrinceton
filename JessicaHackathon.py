from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hi World!'

@app.route('/addevent')
def add_event():
    return 'This will eventually add an event'

@app.route('/eventdetails/<int:eventID>')
def event_detail(eventID):
    return 'findEvent: ' + str(eventID)

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
