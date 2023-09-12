from flask import render_template,redirect,request,session
from flask_app import app
from flask_app.controllers import chefs
from flask_app.controllers import users
from flask_app.controllers import desserts
from flask_app.controllers import requests


if __name__ == "__main__":
    app.run(debug=True)