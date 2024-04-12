from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.request import Request
from flask_app.models.user import User


# CREATE DESSERT..................
@app.route('/requests/new')
def new_request():
    if 'user_id' not in session:
        return redirect('/')
    user=User.get_one(session['user_id'])
    return render_template('create_request.html', user=user)

@app.route('/requests/create', methods=['POST'])
def create_request():
    if 'user_id' not in session:
        return redirect('/')
    if not Request.validate_request(request.form):
        return redirect ('/requests/new')
    data = {
        "user_id":session["user_id"],
        "request_name":request.form["request_name"],
        "request_description":request.form["request_description"]
        }
    Request.save(data)
    return redirect('/user_dash')


# DISPLAY ONE request.............
@app.route('/requests/view/<int:id>')
def display_request(id):
    if 'user_id' not in session:
        return redirect('/')
    # requests=Request.get_request_with_owner(id)
    user=User.get_one(session['user_id'])
    return render_template('display_request.html', requests=requests, user=user)

# DISPLAY ALL REQUESTS...................
@app.route('/requests/view_all')
def view_all_requests():
    if 'user_id' not in session:
        return redirect('/')
    requests=Request.get_all()
    user=User.get_one(session['user_id'])
    return render_template('display_all_requests.html', requests=requests, user=user)


# EDIT request INFORMATION.............
@app.route('/requests/edit/<int:id>')
def edit_request(id):
    if 'user_id' not in session:
        return redirect('/')
    request = Request.get_one(id)
    user=User.get_one(session['user_id'])
    return render_template('edit_request.html', request=request, user=user)


# UPDATE request (POST) using a hidden input..................
@app.route('/requests/update', methods=['POST'])
def update_request():
    if 'user_id' not in session:
        return redirect('/')
    if not Request.validate_request(request.form):
        request_id = request.form['id']
        return redirect(f'/requests/edit/{request_id}')
    data = {
        "user_id":session["user_id"],
        "id":request.form['id'],
        "request_name":request.form["request_name"],
        "request_description":request.form["request_description"]
        }
    Request.update(data)
    return redirect('/user_dash')

# REMOVE FROM WALL (CHEFS)...................
@app.route('/requests/remove/<int:id>')
def remove_request(id):
    if 'chef_id' not in session:
        return redirect('/')
    Request.remove_from_wall(id)
    return redirect('/chef_dash')

# DELETE request...............
@app.route('/requests/delete/<int:id>')
def delete_request(id):
    if 'user_id' not in session:
        return redirect('/')
    Request.delete(id, session['user_id'])
    return redirect('/user_dash')