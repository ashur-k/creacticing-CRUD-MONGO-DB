import os
from flask import Flask, render_template, url_for, request, session, redirect, jsonify, flash
from flask_pymongo import PyMongo
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId


app = Flask(__name__)
app.secret_key = os.getenv("SECRET", "randomstring123")

app.config['MONGO_DBNAME'] = 'kitchen_guide'
app.config['MONGO_URI'] = 'mongodb+srv://root:r00tUser@cluster0-dllo5.mongodb.net/kitchen_guide?retryWrites=true&w=majority'

mongo = PyMongo(app)


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('userinfo'))
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    password_entered = request.form['password']
    if login_user:
        if pbkdf2_sha256.verify(password_entered, login_user['password']):
            session['username'] = request.form['username']
            return redirect(url_for('userinfo'))
    else:
        flash(u'Invalid password provided', 'error')
        return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hash = pbkdf2_sha256.hash(request.form['password'])
            users.insert({'name': request.form['username'], 'password': hash})
            session['username'] = request.form['username']
            return render_template('additional_reg_info.html',
                                    name=mongo.db.users.find_one(
                                    {"name":request.form['username']}))
        flash('User name already exist')
    return render_template('register.html')


@app.route('/insert_additional_info', methods=['POST'])
def insert_additional_info():
    users_account_info = mongo.db.users_account_info
    users_account_info.insert_one(request.form.to_dict())
    return redirect(url_for('userinfo'))


@app.route('/userinfo')
def userinfo():
    return render_template('user_info.html',
                           users_account_info=mongo.db.users_account_info.find_one(
                               {'name': session['username']}))


@app.route('/signout')
def signout():
    session.clear()
    return redirect('/')


@app.route('/edit_user_info/<users_id>')
def edit_user_info(users_id):
    users_info = \
        mongo.db.users_account_info.find_one({'_id': ObjectId(users_id)})
    user = mongo.db.users.find_one({'name': session['username']})
    return render_template('edit_user_info.html', info=users_info,
                           users_login_details=user)


@app.route('/update_user_info/<user_id>', methods=['POST'])
def update_user_info(user_id):
    user_info = mongo.db.users_account_info
    user_info.update({'_id': ObjectId(user_id)}, {
        'name': request.form.get('name'),
        'date_of_birth': request.form.get('date_of_birth'),
        'hobby': request.form.get('hobby'),
        'favourite_moive': request.form.get('favourite_moive'),
        })
    return redirect(url_for('userinfo'))


@app.route('/delete_account/<users_id>')
def delete_account(users_id):
    mongo.db.users.remove({'name': session['username']})
    mongo.db.users_account_info.remove({'_id': ObjectId(users_id)})
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True
    )
