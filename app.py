from flask import Flask, render_template, jsonify, request, redirect
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
app = Flask(__name__)


class TODO:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB URI
        self.db = client['flask']  # Select the 'awb-config' database
        self.collection = self.db['todo data']  # Select the 'companies' 
    
    def create(self, dict):
        document = self.collection.insert_one(dict)

    def read(self):
        document =list(self.collection.find())
        return document
    
    def delete(self, id):
        object_id = ObjectId(id)
        document = self.collection.delete_one({"_id": object_id})
    
    def find(self, id):
        object_id = ObjectId(id)
        document = self.collection.find_one({"_id": object_id})
        return document
    
    def update(self, id, dict):
        object_id = ObjectId(id)
        result = self.collection.update_one(
            {"_id": object_id}, 
            {"$set": dict}  
        )
    
    
@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        time = datetime.now()
        todo = TODO()
        todo.create({"title":title, "desc":desc, "Time":time})
    todo = TODO()
    document = todo.read()
    for user in document:
        user["_id"] = str(user["_id"])
    return render_template("index.html", allTodo = document)

@app.route('/Delete/<string:_id>')
def delete(_id):
    todo = TODO()
    document = todo.delete(str(_id))
    return redirect("/")

@app.route('/Update/<string:_id>', methods=['POST', 'GET'])
def update(_id):
    if request.method == 'POST':
        todo = TODO()
        title = request.form['title']
        desc = request.form['desc']
        time = datetime.now()
        todo.update(_id,{"title":title, "desc":desc, "Time":time})
        return redirect("/")
    todo = TODO()
    document = todo.find(str(_id))
    return render_template("update.html", Todo = document)

if __name__ == '__main__':
    app.run(debug=True)
