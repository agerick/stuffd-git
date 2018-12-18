#models.py

#!myvenv/bin/python
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import ijson
import os
import pandas as pd
import sqlite3
from fuzzywuzzy import fuzz
from utils import clean_unit, clean_id, clean_ingredients
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
#from hashlib import md5

db_name='stuffd.db'

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from flask_restful import Resource, Api

api = Api(app)
############################## Database models


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    instructions = db.Column(db.Text)
    vegetarian = db.Column(db.Boolean)
    glutenFree = db.Column(db.Boolean)
    dairyFree = db.Column(db.Boolean)
    sourceUrl = db.Column(db.String(255))
    pricePerServing = db.Column(db.Float)
    readyInMinutes = db.Column(db.Integer)
    servings = db.Column(db.Float)
    image = db.Column(db.String(255))

    
    # ... any other fields
    ingredients = db.relationship("Ingredient", secondary="association")
    #return the nutrition information
    def get_nutrition(self):
        value_dict={}
        #unit_dict={}
        for assoc in self.association:    
            amount = assoc.amount *(1.0/100.0)
            if assoc.unit != 'grams':
                multiplier = 0
                for weight in assoc.ingredient.weights:
                    if assoc.unit == weight.msre_unit:
                        multiplier = weight.grams / weight.amount
                if multiplier == 0:
                    # set some kind of default value
                    multiplier = 1
                amount = amount * multiplier
            for nd in assoc.ingredient.nutrient_data:
                value_dict[nd.nutrient_obj.name] = value_dict.get(nd.nutrient_obj.name, 0.0) + (amount*nd.amount)
                #unit_dict[nd.nutrient_obj.name] = unit_dict.get(nd.nutrient_obj.name, nd.nutrient_obj.units) 
        return value_dict #, unit_dict
    
    def get_igd_list(self):
        igd_list = []
        for assoc in self.association:
            igd = {
                'name':assoc.ingredient.name,
                'amount':assoc.amount,
                'unit':assoc.unit
            }
            igd_list.append(igd)
        return igd_list
    def get_json(self):
        my_dict = {
            'id':self.id,
            'name':self.title ,
            'instructions':self.instructions,
            'vegetarian':self.vegetarian,
            'glutenFree':self.glutenFree,
            'dairyFree':self.dairyFree,
            'sourceUrl':self.sourceUrl,
            'price':round(self.pricePerServing *(1.0/100.0),2),
            'readyInMinutes':self.readyInMinutes,
            'servings':self.servings,
            'image':self.image,
            'nutrition':self.get_nutrition(),
            'igd_list':self.get_igd_list()
        }
        return my_dict

        

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    aisle = db.Column(db.String(255))
    consistency = db.Column(db.String(255))
    image = db.Column(db.String(255))
    # ... any other fields
    recipes = db.relationship("Recipe", secondary="association")
    nutrients = db.relationship("Nutrient", secondary="nutrient_data")
    
    def say_hi(self):
        print("I am saying hi!")
        print(self.consistency)
        
    def get_nutrient_list(self):
        nutrient_list = []
        for nd in self.nutrient_data:
            one_nutrient = {
            "amount": nd.amount,
            "units": nd.nutrient_obj.units,
            "nutrient": nd.nutrient_obj.name
            }
            nutrient_list.append(one_nutrient)
        return nutrient_list

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def check_password(self, password):
        return True


class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'
    quantity = db.Column(db.Integer)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    recipe = db.relationship(Recipe, backref=db.backref(
        "association", cascade="all, delete-orphan"))
    user = db.relationship(User, backref=db.backref(
        "association", cascade="all, delete-orphan"))



class Association(db.Model):
    __tablename__ = 'association'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'))
    amount = db.Column(db.Float)
    unit = db.Column(db.String(255))
    # ... any other fields
    recipe = db.relationship(Recipe, backref=db.backref(
        "association", cascade="all, delete-orphan"))
    ingredient = db.relationship(Ingredient, backref=db.backref(
        "association", cascade="all, delete-orphan"))

class Weight(db.Model):
    __tablename__ = 'weight'
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), primary_key=True)
    # Sequence number to make a composite primary key
    seq = db.Column(db.Integer, primary_key=True)
    # Unit modifier (for example, 1 in "1 cup").
    amount = db.Column(db.Float, nullable = False)
    # Description (for example, cup, diced, and 1-inch pieces).
    msre_unit = db.Column(db.String(84), nullable = False)
    # Gram weight
    grams = db.Column(db.Float, nullable = False)
    # Number of data points
    num_Data_Pts = db.Column(db.Integer, nullable = True)
    # Standard deviation
    std_Dev = db.Column(db.Float, nullable = True)
    ingredient = db.relationship("Ingredient", backref = "weights")
    
class Nutrient(db.Model):
    __tablename__ = 'nutrients'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), nullable = False)
    # Units of measure (mg, g, g, and so on).
    units = db.Column(db.String(7), nullable = False)
    #nutrient_data = db.relationship("NutrientData", backref="nutrient_obj")
    ingredients = db.relationship("Ingredient", secondary="nutrient_data")

    
class SourceCode(db.Model):
    __tablename__ = 'source_code'
    # 2-digit code
    id = db.Column(db.Integer, primary_key = True)
    # Description of source code that identifies the type of nutrient data.
    description = db.Column(db.String(60), nullable = False)
    nutrient_data = db.relationship("NutrientData", backref="source_code_objects")
    
class NutrientData(db.Model):
    __tablename__ = 'nutrient_data'
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'),primary_key=True)
    nutrient_id = db.Column(db.Integer, db.ForeignKey('nutrients.id'), primary_key=True)
    # Amount in 100 grams, edible portion 
    amount = db.Column(db.Float, nullable = False)
    # If the number of data points is 0, the value was calculated or imputed.
    number_of_data_points = db.Column(db.Integer, nullable = False)
    std_Error = db.Column(db.Float, nullable = True)
    # Code indicating type of data.
    source_code = db.Column(db.Integer, db.ForeignKey('source_code.id'))
    # Number of studies
    number_of_studies = db.Column(db.Integer, nullable = True)
    # Minimum values
    minVal = db.Column(db.Float, nullable = True)
    # Maximum value
    maxVal = db.Column(db.Float, nullable = True)
    nutrient_obj = db.relationship(Nutrient, backref=db.backref(
        "nutrient_data", cascade="all, delete-orphan"))
    ingredient = db.relationship(Ingredient, backref=db.backref(
        "nutrient_data", cascade="all, delete-orphan"))
    
class DataSource(db.Model):
    __tablename__ = 'data_sources'
    # Unique number identifying the reference/source.
    id = db.Column(db.String(8), primary_key = True)
    publication = db.Column(db.String(255))

class DataSourceLink(db.Model):
    __tablename__ = 'data_source_link'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    nutrient_id = db.Column(db.Integer, primary_key=True)
    data_source_id = db.Column(db.String(8),db.ForeignKey('data_sources.id'), primary_key=True)
    __table_args__ = (db.ForeignKeyConstraint([ingredient_id, nutrient_id],
                                           [NutrientData.ingredient_id, NutrientData.nutrient_id]),
                      {})
    ingredient = db.relationship("DataSource", backref = "data_source_link")
    
######################################
db.create_all()
######################################

def add_recipe_to_db(rec_json):
    if 'image' not in rec_json:
        return
    recipe_object = Recipe.query.filter_by(id=rec_json['id']).first()
    if recipe_object is None:
        recipe_object = Recipe(
            id=rec_json['id'], 
            title=rec_json['title'],
            instructions = rec_json['instructions'],
            vegetarian = rec_json['vegetarian'],
            glutenFree = rec_json['glutenFree'],
            dairyFree = rec_json['dairyFree'],
            sourceUrl = rec_json['sourceUrl'],
            pricePerServing = rec_json['pricePerServing'],
            readyInMinutes = rec_json['readyInMinutes'],
            servings = rec_json['servings'],
            image = rec_json['image']
            )
        with db.session.no_autoflush:
            for igd in (clean_ingredients(rec_json['extendedIngredients'])):
                association_object = Association(amount = igd['measures']['metric']['amount'], unit=clean_unit(igd['measures']['metric']['unitLong']))
                ingredient_object = Ingredient.query.filter_by(id=clean_id(igd['id'])).first()
                if ingredient_object is None:
                    ingredient_object = Ingredient(id=clean_id(igd['id']), name=igd['name'], aisle=igd['aisle'],consistency=igd['consitency'],image=igd['image'] ) # make the ingredient object
                association_object.ingredient = ingredient_object
                recipe_object.association.append(association_object)
        db.session.add(recipe_object)
        db.session.commit()  

def add_all_json_recipes():
    filename_list = [
        #'100recipes01.json',
        '100recipes02.json',
        #'100recipes03.json',
        '100recipes04.json',
        #'100recipes05.json',
        '100recipes06.json',
        #'100recipes07.json',
        '100recipes08.json',
        #'100recipes09.json',
        '100recipes10.json'
    ]
    for filename in filename_list:
        fullname = os.path.join('./data_json/', filename)
        with open(fullname, "r") as read_file:
            recipe_list = json.load(read_file)['recipes']
        for recipe in recipe_list:
            add_recipe_to_db(recipe)

def get_trimmed_weight_table():
    fullname = './data_json/weight.json'
    with open(fullname, "r") as read_file:
        row_list = json.load(read_file)
    new_list = []
    for row in row_list:
        igd_id = str(int(row['NDB_No']))
        search_term = row['Msre_Desc']
        unit_list = set([k.unit for k in Association.query.filter_by(ingredient_id=igd_id).all()])
        if ('tbsp' in search_term) and ('tbsp' not in unit_list):
            continue
        if 'tsp' in search_term and 'tsp' not in unit_list:
            continue
        if (unit_list != set()) and (unit_list != set(['grams'])):
            max_value = 0
            for unit in unit_list:
                score = fuzz.partial_ratio(search_term.lower(), unit.lower())
                if score > max_value:
                    max_unit = unit
                    max_value = score
            if max_value > 55:
                row['Msre_Desc'] = max_unit
                row['NDB_No'] = igd_id
                new_list.append(row)

                #print('Search: ' + str(search_term))
                #print("from " + str(unit_list))
                #print("Chose: " + str(max_unit) + " with value: " + str(max_value))
                #print("-----")
    return new_list    

def add_weights_to_db(weight_list):
    for row in weight_list:
        weight_object = Weight(
            ingredient_id=int(row['NDB_No']),
            seq = int(row['Seq']),
            amount = float(row['Amount']),
            msre_unit = row['Msre_Desc'],
            grams = float(row['Gm_Wgt'])
            )
        if row['Num_Data_Pts'] != '':
            weight_object.num_Data_Pts = int(row['Num_Data_Pts'])
        if row['Std_Dev'] != '':
            weight_object.std_Dev = float(row['Std_Dev'])
        db.session.add(weight_object)
        db.session.commit()

def get_nutrient_definitions():
    conn = sqlite3.connect('./data_sql/nutrients.db')
    cur = conn.cursor()
    cur.execute("SELECT Nutr_No, Units, NutrDesc from nutr_def")
    rows = cur.fetchall()
    for row in rows:
        nutrient_object = Nutrient(id=str(row[0]), units=row[1], name=row[2])
        db.session.add(nutrient_object)
        db.session.commit()


def get_source_code():
    conn = sqlite3.connect('./data_sql/nutrients.db')
    cur = conn.cursor()
    cur.execute("SELECT Src_Cd, SrcCd_Desc from src_cd")
    rows = cur.fetchall()
    for row in rows:
        obj = SourceCode(id=str(row[0]), description=row[1])
        db.session.add(obj)
        db.session.commit()

def get_nut_data():
    conn = sqlite3.connect('./data_sql/nutrients.db')
    cur = conn.cursor()
    cur.execute("SELECT NDB_No, Nutr_No, Nutr_Val, Num_Data_Pts, Std_Error, Src_Cd,Num_Studies , Min, Max from nut_data")
    rows = cur.fetchall()
    trim_rows = []
    igd_ids = [k.id for k in Ingredient.query.all()]
    for row in rows:
        if int(row[0]) in igd_ids:
            trim_rows.append(row)
    for row in trim_rows:
        obj = NutrientData(
            ingredient_id=int(row[0]),
            nutrient_id= int(row[1]),
            amount=float(row[2]),
            number_of_data_points=int(row[3])
        )
        if row[4] is not '':
            obj.std_Error=float(row[4])
        if row[5] is not '':
            obj.source_code=int(row[5])
        if row[6] is not '':
            obj.number_of_studies=int(row[6])
        if row[7] is not '':
            obj.minVal=float(row[7])
        if row[8] is not '':
            obj.maxVal=float(row[8])
        
        db.session.add(obj)
    db.session.commit()

def get_data_sources():
    conn = sqlite3.connect('./data_sql/nutrients.db')
    cur = conn.cursor()
    cur.execute("SELECT dataSrc_ID, authors, title, year from data_src")
    rows = cur.fetchall()
    for row in rows:
        id = row[0]
        author = row[1]
        title = row[2]
        year = row[3]
        if title[-1] != '.':
            title = title + '.'
        publication = title + ' ' + author + '. ' + year + '.'
        obj = DataSource(id = id, publication=publication)
        db.session.add(obj)
    db.session.commit()


def get_data_source_link():
    conn = sqlite3.connect('./data_sql/nutrients.db')
    cur = conn.cursor()
    cur.execute("SELECT NDB_No, Nutr_No, DataSrc_ID from datsrcln")
    rows = cur.fetchall()
    trim_rows = []
    igd_ids = [k.id for k in Ingredient.query.all()]
    #nl = [(k.ingredient_id, k.nutrient_id) for k in NutrientData.query.all()]
    for row in rows:
        if int(row[0]) in igd_ids:
            trim_rows.append(row)
    for row in trim_rows:
        obj = DataSourceLink(
            ingredient_id=int(row[0]),
            nutrient_id= int(row[1]),
            data_source_id=row[2]
        )
        db.session.add(obj)
    db.session.commit()


def build_db():
    add_all_json_recipes()
    weight_list = get_trimmed_weight_table()
    add_weights_to_db(weight_list)
    get_nutrient_definitions()
    get_source_code()
    get_nut_data()
    get_data_sources()
    get_data_source_link()


#######################################################

from flask import jsonify, abort, request, send_from_directory
from flask_cors import CORS
from flask_restful import Resource, Api



cwd = os.getcwd()

# set the project root directory as the static folder, you can set others.
CORS(app)


with open('./data_json/products.json') as json_file:
    d = json.load(json_file)

@app.route('/products')
def get_products():
	return jsonify(d)


@app.route('/logo')
def send_logo():
    return send_from_directory(directory=cwd,filename='logo.png')

# Basic route

# @app.route('/hi')
# def index():
# 	return "Hello, World"

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class RecipeResource(Resource):
	def get(self):
		rec_list = []
		for rec in Recipe.query.all()[0:80]:
			rec_list.append(rec.get_json())
		return jsonify(rec_list)

class RecipeSearch(Resource):
    def get(self, search_term):
        rec_list = []
        results_list = Recipe.query.filter(Recipe.title.like('%'+search_term+'%')).all()
        for rec in results_list:
            rec_list.append(rec.get_json())
        return jsonify(rec_list)

        # serialize and return items...

api.add_resource(HelloWorld, '/')
api.add_resource(RecipeResource, '/recipe')

api.add_resource(RecipeSearch, '/search/<search_term>')


######################################
if __name__=='__main__':
    #db.drop_all()
    db.create_all()
    app.run(debug=True)