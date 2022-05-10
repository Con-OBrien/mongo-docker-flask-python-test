"""
1. Registration of a User for 0 token

2. Each user gets 10 tokens

3. Store a sentence on our database for 1 token

4. Retrieve his stored sentence on our database for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def post(self):
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"]

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store UN & PW into database
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 6,
        })

        retJson = {
            "Status": 200,
            "Message: ": 'You successfully signed up for the API'
        }
        return jsonify(retJson)
def verifyPw(username, password):
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]
    return tokens

class Store(Resource):
    def post(self):
        #1. get the posted data
        postedData = request.get_json()
        #2. read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]


        #3. Verify pw match
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)

        #4. Verify token
        num_tokens = countTokens(username)

        if num_tokens<=0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)
        #5. Store sentence and return 2000K
        users.update_one({
            "Username": username,
        }, {
            "$set":{
                "Sentence":sentence,
                "Tokens":num_tokens-1
                }
        })

        retJson = {
            "status": 200,
            "message": 'Sentence saved successfully'
        }
        return jsonify(retJson)

class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302
            }
            return jsonify(retJson)

        num_tokens = countTokens(username)
        if num_tokens<=0:
            retJson = {
                "status": 301
            }
            return jsonify(retJson)
        #Make user pay
        users.update_one({
            "Username": username,
        }, {
            "$set":{
                "Tokens":num_tokens-1
                }
        })


        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        retJson = {
            "status":200,
            "sentence": sentence
        }
        return jsonify(retJson)

api.add_resource(Get, '/get')
api.add_resource(Register, '/register')
api.add_resource(Store, '/store')

if __name__=="__main__":
    app.run(host='0.0.0.0')



""""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert_one({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        prev_num += 1
        UserNum.update_one({}, {"$set":{"num_of_users":prev_num}})
        return str("Hello User " + str(prev_num))

def checkPostedData(postedData, functionName):
    if(functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301 #Missing parameter
        else:
            return 200
    elif functionName == "division":
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"])==0:
            return 302
        else:
            return 200



class Add(Resource):
    def post(self):
        #if I am here, then the resource Add was requested using method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Step 1b: Verify validity of data
        status_code = checkPostedData(postedData, "add")
        if(status_code != 200):
            retJson = {
            "Message": "An error has occurred!",
            "Status Code":status_code
            }
            return jsonify(retJson)

        #If I am herem then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Subtract posted data
        ret = x+y
        retMap = {
         'Message':ret,
         'Status Code': 200
        }
        return jsonify(retMap)


class Subtract(Resource):
    #if I am here, then the resource Subtract was requested using method POST

    #Step 1: Get posted data:
    def post(self):
        postedData = request.get_json()

        #Step 1b: Verify validity of data
        status_code = checkPostedData(postedData, "subtract")
        if(status_code != 200):
            retJson = {
            "Message": "An error has occurred!",
            "Status Code":status_code
            }
            return jsonify(retJson)

        #If I am herem then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        ret = x-y
        retMap = {
         'Message':ret,
         'Status Code': status_code
        }
        return jsonify(retMap)

class Multiply(Resource):
        #if I am here, then the resource Subtract was requested using method POST

        #Step 1: Get posted data:
        def post(self):
            postedData = request.get_json()

            #Step 1b: Verify validity of data
            status_code = checkPostedData(postedData, "multiply")
            if(status_code != 200):
                retJson = {
                "Message": "An error has occurred!",
                "Status Code":status_code
                }
                return jsonify(retJson)

            #If I am herem then status_code == 200
            x = postedData["x"]
            y = postedData["y"]
            x = int(x)
            y = int(y)
            ret = x*y
            retMap = {
             'Message':ret,
             'Status Code': status_code
            }
            return jsonify(retMap)


class Divide(Resource):
        #if I am here, then the resource Subtract was requested using method POST

        #Step 1: Get posted data:
        def post(self):
            postedData = request.get_json()

            #Step 1b: Verify validity of data
            status_code = checkPostedData(postedData, "division")
            if(status_code != 200):
                retJson = {
                "Message": "An error has occurred!",
                "Status Code":status_code
                }
                return jsonify(retJson)

            #If I am herem then status_code == 200
            x = postedData["x"]
            y = postedData["y"]
            x = int(x)
            y = int(y)
            ret = x*1.0/y
            retMap = {
             'Message':ret,
             'Status Code': status_code
            }
            return jsonify(retMap)


api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")
api.add_resource(Visit, "/hello")

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/bye')
def bye():
    #Prepare a response for a request that came to /bye
    c = 2*521
    s = str(c)
    #c = 1/0
    age = 24
    retJson = {
        'Name':'Conor',
        'Age':age,
        'Pets':[
            {
                'petName': 'Buddy',
                'age': 14
            },
            {
                'petName': 'Miley',
                'age': 13
            }
        ]
    }

    return jsonify(retJson)


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
"""
