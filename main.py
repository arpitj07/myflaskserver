from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo

from utils import encryptPass, decryptPass, genID
import uuid
import os

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://aspjain07:password_12345@my-cluster-00.hsnz2cn.mongodb.net/UserDataBase?retryWrites=true&w=majority'

mongo = PyMongo(app)

CORS(app)
db = mongo.db.UserEventCollection

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

# Route for sign up 
@app.route("/register", methods=['POST'])
def register():
    if request.method=='POST':
        user = db.find_one({'userEmail': request.json['userEmail']})
        if(not user):
            encrypted_password = encryptPass(request.json['userPassword'])
            db.insert_one({'userName': request.json['userName'], 'userEmail': request.json['userEmail'],'password':encrypted_password , 'Task': []})
            return jsonify({'status': 'ok', 'message': 'successfully registered'})
        else:
            return jsonify({'status': 'error', 'message': 'Email already exist'})


#Login Route
@app.route("/login", methods=[ 'POST'])
def login():
    if request.method=='POST':
        user = db.find_one({'userEmail': request.json['email']})
        if(user):
            if(decryptPass(request.json['userPassword'], user['password'])):
                return jsonify({'status': 'ok', 'message': 'login successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Wrong credentials'})


# Routes to add events to the event list
@app.route("/addEvent", methods=['POST'])
def addEvent():
    if request.method=='POST':
        db.update_one({'userEmail': request.json['userEmail']}, {'$push': { 'Task': {'TId':str(uuid.uuid4()),'Date': request.json['date'],'StartTime': request.json['startTime'], 'EndTime': request.json['endTime'], 'Event': request.json['eventText'],'Status': 'Not Finished'}}})
                    
        return jsonify({'status': 'ok', 'message': 'Event added successfully'})
    

# Routes for deleting the events
@app.route("/deleteEvent", methods=['POST'])
def deleteEvent():
    print(request.json['id'])
    if request.method=='POST':
        db.find_one_and_update({'userEmail': request.json['userEmail']},{'$pull' : { 'Task' : { 'TID': request.json['id']}} })
        return jsonify({'status': 'ok', 'message': 'Event deleted'})


# Routes for marking events as complete
@app.route("/completeEvent", methods=['POST'])
def complete():
    if request.method=='POST':
        db.find_one_and_update({'userEmail': request.json['userEmail']},{'$push' : { 'Task' : { 'Status': 'Complete'}} })
        return jsonify({'status': 'ok', 'message': 'Event deleted'})


# Routes for getting user details 
@app.route("/userDetails/<userEmail>", methods=['GET'])
def getUsers(userEmail):
    if request.method=='GET':
        user = db.find_one({'userEmail': userEmail})
        return user['Task']



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
