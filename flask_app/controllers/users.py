from flask import render_template,request, redirect, flash, session
from flask_app.models.user import User
from flask_app.models.chef import Chef
from flask_app.models.dessert import Dessert
from flask_app import app
from flask_bcrypt import Bcrypt
import secrets

bcrypt = Bcrypt(app)



# CREATE USER...........................
@app.route('/user_signup')
def create_user():
    return render_template('create_user.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    if not User.validate_user(request.form):
        return redirect("/user_signup")
    email = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(email)
    if user_in_db:
        flash("An account is already using that email. Please use another email address.")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "username": request.form['username'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/user_dash")


# USER DASHBOARD.............
@app.route('/user_dash')
def user_dash():
    if 'user_id' not in session:
        return redirect('/')
    user=User.get_one(session['user_id'])
    chef=Chef.get_one(id)
    following_chefs = User.get_following_chefs(session['user_id'])
    desserts = Dessert.get_all()
    rndm_desserts = desserts if len(desserts) <= 8 else secrets.SystemRandom().sample(desserts, 8)
    return render_template('user_dash.html', user=user, chef=chef, following_chefs=following_chefs, rndm_desserts=rndm_desserts)


# EDIT USER....................
@app.route('/users/edit/<int:id>')
def edit_user(id):
    if 'user_id' not in session:
        return redirect ('/')
    user=User.get_one(session['user_id'])
    return render_template('user_edit.html', user=user)

# UPDATE USER.....................
@app.route('/users/update', methods=['POST'])
def update_user():
    if 'user_id' not in session:
        return redirect('/')
    if not User.validate_user_update(request.form):
        user_id = request.form['id']
        return redirect(f'/users/edit/{user_id}')
    data = {
        "id":session["user_id"],
        "username":request.form["username"],
        }
    User.edit_user(data)
    return redirect('/user_dash')


# USER FOLLOW CHEF.............
@app.route('/follow_chef/<int:chef_id>', methods=['POST'])
def follow(chef_id):
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    User.follow_chef(user_id, chef_id)
    return redirect(f'/desserts/view_all/{chef_id}')


# DISPLAY ALL FOLLOWING CHEFS.............
@app.route('/users/<int:user_id>/view_following')
def view_following(user_id):
    if 'user_id' not in session:
        return redirect('/')
    user=User.get_one(session['user_id'])
    chefs = User.get_following_chefs(user_id)
    return render_template('display_following.html', user=user, chefs=chefs)


# USER LOGIN...............
@app.route('/user_login', methods=['POST'])
def login_user():
    data = { "email":request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/user_dash")

# USER LOGOUT...............
@app.route('/user_logout')
def logout_user():
    session.clear()
    return redirect('/')
