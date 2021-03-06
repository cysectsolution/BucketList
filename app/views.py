from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask.ext.pymongo import PyMongo
from flask_wtf import Form
from flask_wtf.file import FileField
from werkzeug import secure_filename
import bcrypt
import json
import requests
from flask import Markup
from app import app
import bson.binary
from io import StringIO
import logging


#connections to the mongo database
app.config['MONGO_DBNAME'] = 'bktlist'
app.config['MONGO_URI'] = 'mongodb://kihara:kihara@ds151752.mlab.com:51752/bktlist'

mongo = PyMongo(app)

class UploadForm(Form):
    file = FileField()

#index page
@app.route('/')
def index():
    return render_template('index.html')

#display login form
@app.route('/login')
def login():        
    return render_template('login.html')

#the bucket list home page
@app.route('/home')
def home():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    
    if ('username' in session):
        if 'items' in user:
            posts = {}
            try:
                if user['items'][0]:
                    posts['post1'] = user['items'][0]
            except Exception:
                pass

            try:
                if user['items'][1]:
                    posts['post2'] = user['items'][1]
            except Exception:
                pass

            try:
                if user['items'][2]:
                    posts['post3'] = user['items'][2]
            except Exception:
                pass
                
            try:
                if user['items'][3]:
                    posts['post4'] = user['items'][3]
            except Exception:
                pass
                
            try:
                if user['items'][4]:
                    posts['post5'] = user['items'][4]
            except Exception:
                pass
                
            try:
                if user['items'][5]:
                    posts['post6'] = user['items'][5]
            except Exception:
                pass

            try:
                if user['items'][6]:
                    posts['post7'] = user['items'][6]
            except Exception:
                pass

            try:
                if user['items'][7]:
                    posts['post8'] = user['items'][7]
            except Exception:
                pass

            try:
                if user['items'][8]:
                    posts['post9'] = user['items'][8]
            except Exception:
                pass

            try:
                if user['items'][9]:
                    posts['post10'] = user['items'][9]
            except Exception:
                pass
                
            return render_template('home.html', data=posts)
        return render_template('home.html', data=None)

    return redirect(url_for('login'))

#login process
@app.route('/login1', methods=['GET', 'POST'])
def login1():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('home'))
        flash(request.form['username'] + ", thats not your password!")
        return redirect(url_for('login'))
    message = Markup("Sorry, the username does not exist")
    flash(message)
    return redirect(url_for('login'))

#register process
@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        form = request.form['confirm']

        if request.form['username'] != "":
            if form != request.form['password']:
                message = Markup('Passwords have to match!')
                flash(message)
                return redirect(url_for('register'))
            elif existing_user is None:
                hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                users.insert({'name':request.form['username'], 'email':request.form['email'], 'password': hashpass})
                session['username'] =  request.form['username']
                return redirect(url_for('login'))

            error = 'That username already exists!'
            return render_template('register.html', error=error)

    return render_template("register.html", error = error)

#details about MyBucketList
@app.route('/about')
def about():
    return render_template('about.html')

#function on storing items in the bucket list
@app.route('/store', methods=['POST', 'GET'])
def store():
    if request.method == 'POST':
        users = mongo.db.users
        user = users.find_one({'name': session['username']})
        post = request.form['details']
        if 'items' not in user:
            user.update({'items' : []})
        if post not in user['items']:
            users.update({'name': request.form['bktName']},{ '$push': {'items': post}})

            message = Markup("Successfully updated")
            flash(message, category = 'success')
            return redirect(url_for('home'))
        else:
            message = Markup("The item is already in your bucket list!")
            flash(message, category = 'error')
            return redirect(url_for('home'))
    return 'something is wrong'

@app.route('/delete1', methods=['POST', 'GET'])
def delete1():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][0] != 0:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][0] }})
            message = Markup("Item one has been successfully deleted")
            flash(message)
            return redirect(url_for('home'))
        
    except Exception:
        pass
    message = Markup("There is no item to delete")
    flash(message, category='error')
    return redirect(url_for('home'))

@app.route('/delete2', methods=['POST', 'GET'])
def delete2():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][1]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][1] }})
            flash("Item two has been successfully deleted")
            return redirect(url_for('home'))
        
    except Exception:
        pass
    flash("There is no item to delete", category='error')
    return redirect(url_for('home'))

@app.route('/delete3', methods=['POST', 'GET'])
def delete3():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][2]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][2] }})
            flash("Item three has been successfully deleted")
            return redirect(url_for('home'))
        
    except Exception:
        pass
    flash("There is no item to delete", category='error')
    return redirect(url_for('home'))

@app.route('/delete4', methods=['POST', 'GET'])
def delete4():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][3]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][3] }})
            flash("Item four has been successfully deleted")
            return redirect(url_for('home'))
        
    except Exception:
        pass
    flash("There is no item to delete", category='error')
    return redirect(url_for('home'))

@app.route('/delete5', methods=['POST', 'GET'])
def delete5():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][4]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][4] }})
            flash("Item five has been successfully deleted")
            return redirect(url_for('home'))
        
    except Exception:
        pass
    flash("There is no item to delete", category='error')
    return redirect(url_for('home'))

@app.route('/delete6', methods=['POST', 'GET'])
def delete6():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][5]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][5] }})
            flash("Item six has been successfully deleted")
            return redirect(url_for('home'))
        
    except Exception:
        pass
    flash("There is no item to delete", category='error')
    return redirect(url_for('home'))

@app.route('/delete7', methods=['POST', 'GET'])
def delete7():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][6]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][6] }})
            flash("Item seven has been successfully deleted")
            return redirect(url_for('home'))
        
    except Exception:
        pass
    flash("There is no item to delete", category='error')
    return redirect(url_for('home'))

@app.route('/delete8', methods=['POST', 'GET'])
def delete8():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][7]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][7] }})
            flash("Item eight has been successfully deleted")
            return redirect(url_for('home'))
        
    except Exception:
        pass
    flash("There is no item to delete", category='error')
    return redirect(url_for('home'))

@app.route('/delete9', methods=['POST', 'GET'])
def delete9():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][8]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][8] }})
            flash("Item nine has been successfully deleted")
            return redirect(url_for('home'))
        
    except Exception:
        pass
    flash("There is no item to delete", category='error')
    return redirect(url_for('home'))

@app.route('/delete10', methods=['POST', 'GET'])
def delete10():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][9]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][9] }})
            flash("Item ten has been successfully deleted")
            return redirect(url_for('home'))
        
    except Exception:
        pass
    flash("There is no item to delete", category='error')
    return redirect(url_for('home'))

@app.route('/edit1', methods=['POST', 'GET'])
def edit1():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    try:
        if user['items'][0]:
            users.update({'name': session['username']},{ '$pull': { 'items': user['items'][0] }})
            flash("Item one has been deleted so that you can provide a new item")
    except Exception:
        pass
    return redirect(url_for('home'))

@app.route('/forgot', methods=['POST','GET'])
def forgot():
    return render_template('forgot.html')

@app.route('/sendPassword', methods=['POST','GET'])
def sendPassword():
    if request.method == 'POST':
        users = mongo.db.users
        emailUser = request.form['email']
        user = users.find_one({'email': emailUser})
        if user is not None:
            emailito = user['password']
            message = Markup(emailito)
            flash('Your password is: ' + message)
            return redirect(url_for('forgot'))
        message = Markup('The email entered does not exist')
        flash(message)
        return redirect(url_for('forgot'))
    return 'something wrong'

def save_file(f):
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    f = request.files['uploaded_file']
    content = (f.read())
    users.files.save(dict(
        content= content,
        ))


@app.route('/profile', methods=['POST'])
def profile():
    users = mongo.db.users
    user = users.find_one({'name': session['username']})
    f = request.files['uploaded_file']
    fid = save_file(f)
    f = users.files.find_one(bson.objectid.ObjectId(fid))
    return f


if  __name__ == '__main__':
	app.secret_key='mysecret'
	app.run(debug=True)