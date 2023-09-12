import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import chef, dessert


class User:
    DB = "aprons_on_schema"
    def __init__(self,data):
        self.id = data['id']
        self.username = data['username']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.chefs=[]
        self.favorites=[]
        self.confirm_pw=None


# CREATE USER..................
    @classmethod
    def save(cls, data):
        query="""
        INSERT INTO users(username, email, password) 
        VALUES (%(username)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)


# GET USER..............
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls, user_id):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        return cls(results[0])


# EDIT USER....................
    @classmethod
    def edit_user(cls,data):
        query = "UPDATE users SET username=%(username)s WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)


# USERS FOLLOW CHEFS.........................
    @classmethod
    def follow_chef(cls, user_id, chef_id):
        query = "INSERT INTO followers (user_id, chef_id) VALUES (%(user_id)s, %(chef_id)s);"
        data = {'chef_id': chef_id,
                'user_id':user_id
                }
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_following_chefs(cls, user_id):
        query = """SELECT * FROM users LEFT JOIN followers ON followers.user_id = users.id 
                LEFT JOIN chefs ON followers.chef_id = chefs.id 
                WHERE users.id = %(id)s"""
        data = {'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        following_chefs = []
        for row in results:
            chef_data= {
                'id': row['chefs.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['chefs.email'],
                'password': row['chefs.password'],
                'freelance': row['freelance'],
                'created_at': row['chefs.created_at'],
                'updated_at': row['chefs.updated_at']
            }
            following_chefs.append((chef_data))
        return following_chefs

# VALIDATE USER..................
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["username"]) < 2:
            flash("Username must be at least 3 characteres.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Password must be at least 8 characteres.")
            is_valid = False
        if (user["confirm_pw"]) != (user["password"]):
            flash("Passwords do not match.")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_user_update(user):
        is_valid = True
        if len(user['username']) < 3:
            flash("Username must be at least 3 characteres.")
            is_valid = False
        return is_valid