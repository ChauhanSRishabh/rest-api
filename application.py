# SET UP FLASK
from flask import Flask, request
app = Flask(__name__)

# ORM
# As the name suggests, we work with it by creating objects
from flask_sqlalchemy import SQLAlchemy

# CONFIGURE DATABASE TO CONNECT TO IT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # That's how we say we are going to create sqlite database called data.db in the same directory
db = SQLAlchemy(app) # db is an instance of SQLAlchemy and then we pass in our flask app

# We define all of the things we want to store in our database as models
class Drink(db.Model): # inherits from db.Model and that's how we can use various built-in functionalities and that's how we can use it with SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable = False) 
    description = db.Column(db.String(120))

    def __repr__(self) -> str:
        # return super().__repr__()
        return f"{self.name} - {self.description} "



# MAKE ENDPOINT AND GIVE IT A PATH
@app.route('/')
def index():
    return "Hello!"


# APP TO STORE DRINKS
# GET data by query.all()
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output = []
    
    for drink in drinks:
        drink_data  = {"name" : drink.name, "description" : drink.description}
        output.append(drink_data)
    
    return {"drinks" : output}


# GET data by id with parameter
# Check this out : https://stackoverflow.com/questions/6845772/should-i-use-singular-or-plural-name-convention-for-rest-resources
# the name convention of stack overflow uses plurals
@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name" : drink.name, "description" : drink.description}


# POST a new record
@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name = request.json['name'], description = request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id':drink.id}

# DELETE data
@app.route('/drinks/<id>', methods=['DELETE'])
def del_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error" : "not found"}
    db.session.delete(drink)
    db.session.commit()
    return {"message" : "pppphssssh!@"}