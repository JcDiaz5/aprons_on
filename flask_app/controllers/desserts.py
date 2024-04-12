from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.dessert import Dessert
from flask_app.models.chef import Chef
from flask_app.models.user import User


# CREATE DESSERT..................
@app.route('/desserts/new')
def new_dessert():
    if 'chef_id' not in session:
        return redirect('/')
    chef=Chef.get_one(session['chef_id'])
    return render_template('create_dessert.html', chef=chef)

@app.route('/desserts/create', methods=['POST'])
def create_dessert():
    if 'chef_id' not in session:
        return redirect('/')
    if not Dessert.validate_dessert(request.form):
        return redirect ('/desserts/new')
    data = {
        "chef_id":session["chef_id"],
        "dessert_name":request.form["dessert_name"],
        "ingredients":request.form["ingredients"],
        "instructions":request.form["instructions"]
        }
    Dessert.save(data)
    return redirect('/chef_dash')


# DISPLAY ONE DESSERT.............
@app.route('/desserts/view/<int:id>')
def display_dessert(id):
    if 'chef_id' not in session and 'user_id' not in session:
        return redirect('/')
    dessert=Dessert.get_one_with_owner(id)
    return render_template('display_dessert.html', dessert=dessert)

#  DISPLAY ALL DESSERTS (SELF CHEF)..........................
@app.route('/desserts/<int:chef_id>/view_all')
def view_all_desserts(chef_id):
    if 'chef_id' not in session:
        return redirect('/')
    desserts=Dessert.get_all_from_chef(session['chef_id'])
    chef=Chef.get_one(session['chef_id'])
    one_dessert = Dessert.get_one(id)
    return render_template('display_all_from_owner.html', one_dessert=one_dessert, desserts=desserts, chef=chef)

# DISPLAY ALL DESSERTS TO USERS................
@app.route('/desserts/users/view_all')
def users_view_all_desserts():
    if'user_id' not in session:
        return redirect('/')
    desserts=Dessert.get_all_desserts()
    user=User.get_one(session['user_id'])
    return render_template('display_all_desserts.html', desserts=desserts, user=user)


# DISPLAY ALL DESSERTS FROM ONE CHEF.................
@app.route('/desserts/view_all/<int:id>')
def desserts_from_chef(id):
    if'user_id' not in session:
        return redirect('/')
    desserts=Dessert.get_all_from_chef(id)
    user=User.get_one(session['user_id'])
    return render_template('display_all_from_owner.html', desserts=desserts, user=user)

# FAVORITE DESSERTS (USERS)....................
@app.route('/desserts/<int:user_id>/favorites')
def view_favorites(user_id):
    if 'user_id' not in session:
        return redirect('/')
    user=User.get_one(session['user_id'])
    desserts = Dessert.get_favorite_desserts(user_id)
    return render_template('display_favorites.html', user=user, desserts=desserts)

@app.route('/add_favorites/<int:dessert_id>', methods=['POST'])
def favorites(dessert_id):
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    Dessert.add_favorite(user_id, dessert_id)
    return redirect(f'/desserts/{user_id}/favorites')

# REMOVE FROM FAVORITES (USERS)...................
@app.route('/favorites/remove/<int:id>')
def remove_favorites(id):
    if 'user_id' not in session:
        return redirect('/')
    user_id = session['user_id']
    Dessert.remove_from_favorites(id)
    return redirect(f'/desserts/{user_id}/favorites')

# EDIT DESSERT INFORMATION (CHEF).............
@app.route('/desserts/edit/<int:id>')
def edit_dessert(id):
    if 'chef_id' not in session:
        return redirect('/')
    dessert = Dessert.get_one(id)
    chef=Chef.get_one(session['chef_id'])
    return render_template('dessert_edit.html', dessert=dessert, chef=chef)


# UPDATE DESSERT (POST) using a hidden input..................
@app.route('/desserts/update', methods=['POST'])
def update_dessert():
    if 'chef_id' not in session:
        return redirect('/')
    if not Dessert.validate_dessert(request.form):
        dessert_id = request.form['id']
        return redirect(f'/desserts/edit/{dessert_id}')
    data = {
        "chef_id":session["chef_id"],
        "dessert_name":request.form["dessert_name"],
        "ingredients":request.form["ingredients"],
        "instructions":request.form["instructions"],
        "id":request.form["id"]
        }
    Dessert.update(data)
    dessert_id = request.form['id']
    return redirect(f'/desserts/view/{dessert_id}')


# DELETE DESSERT...............
@app.route('/desserts/delete/<int:id>')
def delete(id):
    if 'chef_id' not in session:
        return redirect('/')
    Dessert.delete(id, session['chef_id'])
    return redirect('/chef_dash')