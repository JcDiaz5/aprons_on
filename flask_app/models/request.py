from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Request:
    DB = "aprons_on_schema"
    def __init__(self, data):
        self.id = data['id']
        self.request_name = data['request_name']
        self.request_description=data['request_description']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.owner = None


# SAVE REQUEST METHOD...
    @classmethod
    def save(cls, data):
        query = """INSERT INTO requests (request_name, request_description, user_id) 
        VALUES (%(request_name)s, %(request_description)s, %(user_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result


# GET ONE...
    @classmethod
    def get_one(cls, request_id):
        query  = "SELECT * FROM requests WHERE id = %(id)s;"
        data = {'id': request_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def get_request_with_owner(cls, id):
        query = "SELECT * FROM requests JOIN users ON requests.user_id = users.id WHERE requests.id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        one_request = cls(results[0])
        for request in results:
            one_request_creator_info = {
                'id': request['users.id'],
                'username': request['username'],
                'email': request['email'],
                'password': request['password'],
                'created_at': request['created_at'],
                'updated_at': request['updated_at']
                }
            creator = user.User(one_request_creator_info)
            one_request.owner = creator
        return one_request


# UPDATE METHOD...
    @classmethod
    def update(cls,data):
        query = """UPDATE requests 
                SET request_name=%(request_name)s, request_description=%(request_description)s
                WHERE id = %(id)s AND requests.user_id = %(user_id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

# REMOVE FROM WALL............
    @classmethod
    def remove_from_wall(cls, id):
        query  = "DELETE FROM requests WHERE id = %(id)s"
        data = {"id":id}
        return connectToMySQL(cls.DB).query_db(query, data)
    
# DELETE METHOD...
    @classmethod
    def delete(cls, id, user_id):
        query  = "DELETE FROM requests WHERE id = %(id)s AND user_id = %(user_id)s;"
        data = {"id": id, "user_id":user_id}
        return connectToMySQL(cls.DB).query_db(query, data)

# GET ALL
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM requests LEFT JOIN users ON requests.user_id = users.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        if not results:
            return[]
        requests = []
        for request in results:
            one_request = cls(request)
            data = {'id': request['users.id'],
                    'username': request['username'],
                    'email': request['email'],
                    'password': request['password'],
                    'created_at': request['created_at'],
                    'updated_at': request['updated_at']
                    }
            one_request.owner = user.User(data)
            requests.append(one_request)
        return requests
    
    # VALIDATIONS...........
    @staticmethod
    def validate_request(data):
        is_valid = True
        if len(data['request_name']) < 3:
            flash("Request Name must be at least 3 characters.")
            is_valid = False
        if len(data['request_description']) < 5:
            flash("Description must be at least 5 characters.")
            is_valid = False
        return is_valid