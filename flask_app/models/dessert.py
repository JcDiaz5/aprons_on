from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import chef
from flask import flash


class Dessert:
    DB = "aprons_on_schema"
    def __init__(self, data):
        self.id = data['id']
        self.dessert_name = data['dessert_name']
        self.ingredients=data['ingredients']
        self.instructions=data['instructions']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.owner = None


# SAVE TV dessert METHOD...
    @classmethod
    def save(cls, data):
        query = """INSERT INTO desserts (dessert_name, ingredients, instructions, chef_id) 
        VALUES (%(dessert_name)s, %(ingredients)s, %(instructions)s, %(chef_id)s);"""
        result = connectToMySQL(cls.DB).query_db(query,data)
        return result


# GET ONE...
    @classmethod
    def get_one(cls, dessert_id):
        query  = "SELECT * FROM desserts WHERE id = %(id)s;"
        data = {'id': dessert_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM desserts LEFT JOIN chefs ON desserts.chef_id = chefs.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        if not results:
            return[]
        desserts = []
        for row in results:
            one_dessert = cls(row)
            data = {'id': row['chefs.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'freelance':row['freelance'],
                    'created_at': row['chefs.created_at'],
                    'updated_at': row['chefs.updated_at']
                    }
            one_dessert.owner = chef.Chef(data)
            desserts.append(one_dessert)
        return desserts

    @classmethod
    def get_all_from_chef(cls, id):
        query = "SELECT * FROM desserts LEFT JOIN chefs ON desserts.chef_id = chefs.id WHERE chefs.id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        all_desserts = []
        print(f'**********************{results}')
        for row in results:
            one_dessert = cls(row)
            all_desserts_creator_info = {
                "id":row['chefs.id'],
                "first_name":row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'freelance':row['freelance'],
                'created_at': row['chefs.created_at'],
                'updated_at': row['chefs.updated_at']
                }
            one_dessert.owner = chef.Chef(all_desserts_creator_info)
            all_desserts.append(one_dessert)
        return all_desserts
    
    @classmethod
    def get_one_with_owner(cls, id):
        query = "SELECT * FROM desserts JOIN chefs ON desserts.chef_id = chefs.id WHERE desserts.id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL(cls.DB).query_db(query,data)
        one_dessert = cls(results[0])
        for row in results:
            one_dessert_creator_info = {
                "id":row['chefs.id'],
                "first_name":row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'freelance':row['freelance'],
                'created_at': row['chefs.created_at'],
                'updated_at': row['chefs.updated_at']
                }
            creator = chef.Chef(one_dessert_creator_info)
            one_dessert.owner = creator
        return one_dessert

# FAVORITE DESSERTS (USERS)............................
    @classmethod
    def add_favorite(cls, user_id, dessert_id):
        query = "INSERT INTO favorites (user_id, dessert_id) VALUES (%(user_id)s, %(dessert_id)s);"
        data = {'dessert_id': dessert_id,
                'user_id':user_id
                }
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_favorite_desserts(cls, user_id):
        query = """SELECT * FROM users LEFT JOIN favorites ON favorites.user_id = users.id 
                LEFT JOIN desserts ON favorites.dessert_id = desserts.id 
                WHERE users.id = %(id)s;"""
        data = {'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        favorite_desserts = []
        for row in results:
            dessert_data= {
                'id': row['desserts.id'],
                'dessert_name': row['dessert_name'],
                'ingredients': row['ingredients'],
                'instructions': row['instructions'],
                'created_at': row['desserts.created_at'],
                'updated_at': row['desserts.updated_at'],
                'chef_id': row['chef_id']
            }
            favorite_desserts.append((dessert_data))
        return favorite_desserts

# UPDATE METHOD...
    @classmethod
    def update(cls,data):
        query = """UPDATE desserts 
                SET dessert_name=%(dessert_name)s, ingredients=%(ingredients)s, instructions=%(instructions)s 
                WHERE id = %(id)s AND desserts.chef_id = %(chef_id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)

# REMOVE FROM FAVORITES............
    @classmethod
    def remove_from_favorites(cls, id):
        query  = "DELETE FROM favorites WHERE dessert_id = %(dessert_id)s"
        data = {"dessert_id":id}
        return connectToMySQL(cls.DB).query_db(query, data)

# DELETE METHOD...
    @classmethod
    def delete(cls, id, chef_id):
        query  = "DELETE FROM desserts WHERE id = %(id)s AND chef_id = %(chef_id)s;"
        data = {"id": id, "chef_id":chef_id}
        return connectToMySQL(cls.DB).query_db(query, data)


# GET ALL FOR DASHBOARD
    @classmethod
    def get_all_desserts(cls):
        query = "SELECT * FROM desserts LEFT JOIN chefs ON desserts.chef_id = chefs.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        if not results:
            return[]
        desserts = []
        for dessert in results:
            one_dessert = cls(dessert)
            data = {'id': dessert['chefs.id'],
                    'first_name': dessert['first_name'],
                    'last_name': dessert['last_name'],
                    'email': dessert['email'],
                    'password': dessert['password'],
                    'freelance':dessert['freelance'],
                    'created_at': dessert['chefs.created_at'],
                    'updated_at': dessert['chefs.updated_at']
                    }
            one_dessert.owner = chef.Chef(data)
            desserts.append(one_dessert)
        return desserts
    
    # VALIDATIONS...........
    @staticmethod
    def validate_dessert(data):
        is_valid = True
        if len(data['dessert_name']) < 3:
            flash("Dessert_name must be at least 3 characters.")
            is_valid = False
        if len(data['ingredients']) < 3:
            flash("Ingredients must be at least 3 characters.")
            is_valid = False
        if len(data['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        return is_valid