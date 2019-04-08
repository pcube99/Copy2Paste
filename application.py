##Author : Pankil Panchal
## github : pcube99

#!/usr/bin/env python3
from flask import Flask, render_template, url_for, request, session, redirect,Markup, flash
from flask_pymongo import PyMongo
import os
import sys
import time
##########
#print (os.environ)
#from passlib.hash import sha256_crypt
app = Flask(__name__)
app.config["MONGO_DBNAME"] = "copy2paste"
app.config["MONGO_URI"] = "mongodb://ppp:PANKIL@cluster0-shard-00-00-tqm1v.mongodb.net:27017,cluster0-shard-00-01-tqm1v.mongodb.net:27017,cluster0-shard-00-02-tqm1v.mongodb.net:27017/copy2paste?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"
##
mongo = PyMongo(app)

@app.route('/', methods=['POST', 'GET'])
def paste():
    rows = []
    database = mongo.db.copy2paste
    if(request.method == 'GET'):
        for i in database.find():
            row = {}
            row['title'] = i['title']
            row['content'] = i['content']
            rows.append(row)
        return render_template("index.html",rows=rows)

    elif(request.method == 'POST'):
        return "added"
    else:
        return "return"

@app.route('/add', methods=['POST', 'GET'])
def add():
    if(request.method == 'POST'):
        databas = mongo.db.copy2paste
        if(request.form['paste_title']):
            databas.insert({'title' : request.form['paste_title'], 'content' : request.form['paste_content']})
            return redirect(url_for('paste'))
    return render_template('add.html')

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete(id):
    if(request.method == 'POST'):
        mongo.db.copy2paste.delete_one({"title" : id})
    return redirect(url_for('paste'))

app.secret_key = 'mysecret'

if __name__ == '__main__':  
    app.run(debug=True)
