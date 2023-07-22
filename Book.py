from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'BookMyShow'
app.config['MONGO_URI'] = 'mongodb+srv://tmxsmoke:aminocentesis@cluster0.zmgremb.mongodb.net/BookMyShow?retryWrites=true&w=majority'
mongo = PyMongo(app)


@app.route("/")
def welcome():
    return "Welcome to home page"


data = {
    "title": "",
    "img": "",
    "print": "",
    "language": "",
    "duration": "",
    "about": "",
    "likes": ""


}


def serialize_document(document):
    serialized = dict(document)
    serialized['_id'] = str(serialized['_id'])  # Convert ObjectId to string
    return serialized


@app.route("/PostMovie", methods=["POST"])
def addMovies():
    data = request.get_json()
    print(data)
    collection = mongo.db.movie
    inserted_data = collection.insert_one(data)
    return jsonify("data added successfully")


@app.route("/GetMovies", methods=["GET"])
def GetMovies():
    collection = mongo.db.movie
    data = list(collection.find())
    print(data)
    for i in data:
        i["_id"] = str(i["_id"])
    return jsonify(data)


@app.route("/GetMovies/<string:id>", methods=["GET"])
def GetMoviesById(id):
    collection = mongo.db.movie
    data = list(collection.find({"_id": ObjectId(id)}))
    print(data)
    for i in data:
        i["_id"] = str(i["_id"])
    return jsonify(data)


@app.route("/addcinema", methods=["POST"])
def addCinema():
    data = request.get_json()
    print(data)
    collection = mongo.db.cinema
    inserted_data = collection.insert_one(data)
    return jsonify("data added successfully")


@app.route("/addmovie/<string:id>", methods=["PATCH"])
def addMovie(id):
    print(id)
    data = request.get_json()
    print(data, "line142\n")
    collection = mongo.db.cinema
    val = collection.find_one({"_id": ObjectId(id)})
    print(val)
    if val:
        val["movies"].append(data["movies"])
        val["priceN"].append(data["priceN"])
        val["priceD"].append(data["priceD"])
        val["priceX"].append(data["priceX"])
        val["priceX"].append(data["priceX"])
        val["about_movies"].append(data["about_movies"])
        val["images"].append(data["images"])
        val["time"].append(data["time"])
        inserted_data = collection.update_one({"_id": ObjectId(id)}, {"$set": {"movies": val["movies"], "priceN": val["priceN"],
                                                                               "priceD": val["priceD"],
                                                                               "priceX": val["priceX"],
                                                                               "about_movies": val["about_movies"],
                                                                               "images": val["images"],
                                                                               "time": val["time"]
                                                                               }})

        return jsonify("Movie Added Successfully")
    return jsonify("cinema with this id doesn't exist")


@app.route("/login", methods=["POST"])
def getlogin():
    logindata = request.get_json()
    collection = mongo.db.login
    if logindata["email"] == "admin@gmail.com" and logindata["password"] == "pankaj":
        return jsonify("Welcome Admin", "Pankaj Vashisht")

    login = collection.find_one(
        {"email": logindata["email"], "password": logindata["password"]})
    if login:
        login["_id"] = str(login["_id"])
        return jsonify("Login Successful", login)

    return jsonify("Wrong Credentials", "")


@app.route("/Signup", methods=["POST"])
def getSignup():
    Signup = request.get_json()
    collection = mongo.db.login

    existing_user = collection.find_one({"email": Signup["email"]})
    if existing_user:
        return jsonify("Email already exists")
    else:
     Signup["dob"]=""
     Signup["plans"]="Regular"
     collection.insert_one(Signup)
    return jsonify("Successfully Created Account")





@app.route("/Signup/<string:id>",methods=["PATCH"])
def patchsignup(id):
   
    data=request.get_json()
    print(id,data)
    collection = mongo.db.login
    find=collection.update_one({"_id":ObjectId(id)},{"$set":{"username":data["username"],"dob":data["dob"],"plans":data["plans"]}})
    find2=collection.find_one({"_id":ObjectId(id)})

    
    find2["_id"]=str(find2["_id"])
    return jsonify("data patched succesfully",find2)
   
     














@app.route('/movie/<name>', methods=['GET'])
def single_movie_cinema(name):
    cinema = mongo.db.cinema.find()
    location = request.args.get("location")
    print(f"\n{location}\n")
    cinema_arr = []
    for i in cinema:
        serialized_movies = serialize_document(i)
        cinema_arr.append(serialized_movies)

    arrs = list(cinema_arr)
    arr1 = []
    for i in arrs:
        for j, movie_name in enumerate(i["movies"]):
            if movie_name == name:
                obj = {}
                obj["MovieName"] = movie_name
                obj["about_movie"] = i["about_movies"][j]
                obj["cinemaName"] = i["cinemaName"]
                obj["duration"] = i["duration"][j]
                obj["image"] = i["images"][j]
                obj["language"] = i["language"][j]
                obj["location"] = i["location"]
                obj["priceD"] = i["priceD"][j]
                obj["priceN"] = i["priceN"][j]
                obj["priceX"] = i["priceX"][j]
                obj["rating"] = i["rating"][j]
                obj["time"] = i["time"][j]

                arr1.append(obj)

    arr2=[]
    if location:
        for i in arr1:
            if i["location"] == location:
                arr2.append(i)

        return jsonify(arr2)
    return jsonify(arr1)


@app.route('/cinemas', methods=["GET"])
def get_cinema():
    cinema = mongo.db.cinema.find()
    cinema_arr = []
    for i in cinema:
        serialized_movies = serialize_document(i)
        cinema_arr.append(serialized_movies)

    arrs = list(cinema_arr)
    return (arrs)


@app.route('/add_cinema', methods=["POST"])
def post_cinema():
    if request.method == "POST":
        data = request.get_json()
        cinema = mongo.db.cinema.find()
        cinema_arr = []
        for i in cinema:
            serialized_movies = serialize_document(i)
            cinema_arr.append(serialized_movies)

        arrs = list(cinema_arr)
        for i in arrs:
            if i["cinemaName"] == data["cinemaName"]:
                return jsonify("This cinema is already present")

        mongo.db.cinema.insert_one(data)

        return jsonify("Cinema added successfully")



@app.route("/getLocation/<name>",methods=["GET"])
def getLocation(name):
 print(name)

 cinema = list(mongo.db.cinema.find({"location":location}))
    
 data=[]
 for i in cinema:
     for j in i["movies"]:
         if j==name:
             data.append(i)
             break;
 for i in data:
     i["_id"]=str(i["_id"]) 
     i["time"]=i["time"]
 return jsonify(data)

#  return jsonify(name,location)

if __name__ == '__main__':
    app.run(port=3002)
