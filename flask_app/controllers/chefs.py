from flask import render_template,request, redirect, flash, session
from flask_app.models.chef import Chef
from flask_app.models.request import Request
from flask_app.models.dessert import Dessert
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if "chef_id" in session:
        return redirect('/chef_dash')
    if "user_id" in session:
        return redirect('/user_dash')
    else:
        return render_template('index.html')

# CREATE CHEF...........................
@app.route('/chef_signup')
def create():
    return render_template('create_chef.html')

@app.route('/create_chef', methods=['POST'])
def register():
    if not Chef.validate_chef(request.form):
        return redirect("/chef_signup")
    email = { "email" : request.form["email"] }
    if chef_in_db := Chef.get_by_email(email):
        flash("An account is already using that email. Please use another email address.")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash,
        "freelance": request.form['freelance']
    }
    chef_id = Chef.save(data)
    session['chef_id'] = chef_id
    return redirect("/chef_dash")


# CHEF'S DASHBOARD / DISPLAY REQUESTS.............
@app.route('/chef_dash')
def chef_dash():
    if 'chef_id' not in session:
        return redirect('/')
    chef=Chef.get_one(session['chef_id'])
    desserts=Dessert.get_all_from_chef(session['chef_id'])
    requests=Request.get_all()
    followers=Chef.get_followers(session['chef_id'])
    return render_template('chef_dash.html', chef=chef, desserts=desserts, requests=requests, followers=followers)


# EDIT CHEF.............................
@app.route('/chef/edit/<int:chef_id>')
def edit_chef(chef_id):
    if 'chef_id' not in session:
        return redirect('/')
    chef=Chef.get_one(session['chef_id'])
    return render_template('chef_edit.html', chef=chef)

@app.route('/chef/update', methods=['POST'])
def update():
    if 'chef_id' not in session:
        return redirect('/')
    if not Chef.validate_chef_update(request.form):
        chef_id = request.form['id']
        return redirect(f'/chef/edit/{chef_id}')
    data = {
        "id":session["chef_id"],
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "freelance":request.form["freelance"]
        }
    Chef.update_chef(data)
    return redirect('/chef_dash')

# DISPLAY ALL FOLLOWERS................
@app.route('/chef/<int:chef_id>/followers')
def view_followers(chef_id):
    if "chef_id" in session:
        return redirect('/chef_dash')
    chef = Chef.get_one(session['chef_id'])
    followers = Chef.get_followers(chef_id)
    return render_template('display_followers.html', chef=chef, followers=followers)

# CHEF LOGIN...............
@app.route('/chef_login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    chef_in_db = Chef.get_by_email(data)
    if not chef_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(chef_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['chef_id'] = chef_in_db.id
    return redirect("/chef_dash")

# CHEF LOGOUT...............
@app.route('/chef_logout')
def logout():
    session.clear()
    return redirect('/')
