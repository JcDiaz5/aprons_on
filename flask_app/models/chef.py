import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models import user
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import user, dessert


class Chef:
    DB = "aprons_on_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.freelance=data['freelance']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.desserts=[]
        self.followers=[]
        self.request=[]
        self.confirm_pw=None


# CREATE CHEF..................
    @classmethod
    def save(cls, data):
        query="""
        INSERT INTO chefs(first_name, last_name, email, password, freelance) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(freelance)s);
        """
        return connectToMySQL(cls.DB).query_db(query, data)


# GET CHEF..............
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM chefs WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_one(cls, chef_id):
        query  = "SELECT * FROM chefs WHERE id = %(id)s;"
        data = {'id': chef_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        return cls(results[0])
    
    @classmethod
    def update_chef(cls, data):
        query = """UPDATE chefs
                SET first_name=%(first_name)s, last_name=%(last_name)s, freelance=%(freelance)s 
                WHERE id = %(id)s"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def get_followers(cls, chef_id):
        query = """SELECT * FROM chefs LEFT JOIN followers ON followers.chef_id = chefs.id 
                LEFT JOIN users ON followers.user_id = users.id 
                WHERE chefs.id = %(id)s"""
        data = {'id': chef_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        followers= []
        for row in results:
            user_data= {
                'id': row['users.id'],
                'username': row['username'],
                'email': row['users.email'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            followers.append((user_data))
        return followers

    @classmethod
    def get_request_with_owner(cls, id):
        query = "SELECT * FROM requests JOIN users ON request.user_id = users.id WHERE requests.id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        print(f'###############{results}')
        one_request = cls(results[0])
        for row in results:
            one_show_creator_info = {
                "id":row['users.id'],
                "first_name":row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'freelance': row['freelance'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
                }
            creator = user.User(one_show_creator_info)
            one_request.owner = creator
        return one_request

# VALIDATE CHEF..................
    @staticmethod
    def validate_chef(chef):
        is_valid = True
        if len(chef["first_name"]) < 2:
            flash("First Name must be at least 2 characteres.")
            is_valid = False
        if len(chef["last_name"]) < 2:
            flash("Last Name must be at least 2 characteres.")
            is_valid = False
        if not EMAIL_REGEX.match(chef['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(chef["password"]) < 8:
            flash("Password must be at least 8 characteres.")
            is_valid = False
        if (chef["confirm_pw"]) != (chef["password"]):
            flash("Passwords do not match.")
            is_valid = False
        if len(chef["freelance"]) < 4:
            flash("Freelance must be at least 4 characteres.")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_chef_update(chef):
        is_valid = True
        if len(chef["first_name"]) < 2:
            flash("First Name must be at least 2 characteres.")
            is_valid = False
        if len(chef["last_name"]) < 2:
            flash("Last Name must be at least 2 characteres.")
            is_valid = False
        if len(chef["freelance"]) < 5:
            flash("Feelance field must be at least 5 characteres.")
            is_valid = False
        return is_valid