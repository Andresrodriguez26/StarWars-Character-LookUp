from werkzeug.security import generate_password_hash 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin, LoginManager 
from datetime import datetime
import uuid 
from flask_marshmallow import Marshmallow

# Internal imports
from .helpers import get_character


db = SQLAlchemy() 
login_manager = LoginManager() 
ma = Marshmallow()

#use login_manager object to create a user_loader function
@login_manager.user_loader
def load_user(user_id):

    return User.query.get(user_id) 


class User(db.Model, UserMixin): 
    
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) 


    #INSERT INTO User() Values()
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email 
        self.password = self.set_password(password) 



    #methods for editting our attributes 
    def set_id(self):
        return str(uuid.uuid4())
    

    def get_id(self):
        return str(self.user_id) 
    
    
    def set_password(self, password):
        return generate_password_hash(password)
    

    def __repr__(self):
        return f"<User: {self.username}>"
    



class Product(db.Model): #db.Model helps us translate python code to columns in SQL 
    prod_id = db.Column(db.String, primary_key=True)
    character_name = db.Column(db.String(50), nullable=False)
    homeworld = db.Column(db.String(50))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
    #eventually we need to connect this to orders 

    def __init__(self, price, quantity, character_name):
        self.prod_id = self.set_id()
        self.character_name = character_name
        self.homeworld = self.get_homeworld(character_name)
        self.price = price
        self.quantity = quantity 

    def set_id(self):
        return str(uuid.uuid4())
    
    def get_homeworld(self, name):
        get_both = get_character(name)
        print(get_both)
        return get_both
    

    
    def decrement_quantity(self, quantity):

        self.quantity -= int(quantity)
        return self.quantity
    
    def increment_quantity(self, quantity):

        self.quantity += int(quantity)
        return self.quantity 
    

    def __repr__(self):
        return f"<Product: {self.character_name}>"
    

class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key=True)
    date_created = db.Column(db.String, default=datetime.utcnow())
    # This is how we tie a table to another one (so not a coumn but establishing a relationship)
    prodord = db.relationship('ProdOrder', backref = 'customer', lazy=True) #lazy = True means we dont need the ProdOrder table to have a customer

    def __init__(self, cust_id):
        self.cust_id = cust_id # When a customer makes an order on the frontend they will pass us their cust_id


    def __repr__(self):
        return f"<Customer: {self.cust_id}>"



class ProdOrder(db.Model):
    prodorder_id = db.Column(db.String, primary_key=True)
    prod_id = db.Column(db.String, db.ForeignKey('product.prod_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable = False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable = False)



    def __init__(self, prod_id, quantity, price, order_id, cust_id):
        self.prodorder_id = self.set_id()
        self.prod_id = prod_id
        self.quantity = quantity # How much quantity of that product we want to purchase
        self.price = self.set_price(quantity, price) # So price PER product
        self.order_id = order_id
        self.cust_id = cust_id



    def set_id(self):
        return str(uuid.uuid4())
    


    def set_price(self, quantity, price):

        quantity = int(quantity)
        price = float(price)

        self.price = quantity * price # This total price for that product multiplied by quantity purchased
        return self.price
    

    def update_quantity(self, quantity):

        self.quantity = int(quantity)
        return self.quantity
    


class Order(db.Model):
    order_id = db.Column(db.String, primary_key = True)
    order_total = db.Column(db.Numeric(precision = 10, scale = 2), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodord = db.relationship('ProdOrder', backref = 'order', lazy = True) # Establishing that relationship, NOT A COLUMN



    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00


    def set_id(self):
        return str(uuid.uuid4())
    

    def increment_ordertotal(self, price):

        self.order_total = float(self.order_total) # Just making sure its a float
        self.order_total += float(price)

        return self.order_total
    
    
    def decrement_ordertotal(self, price):

        self.order_total = float(self.order_total) # Just making sure its a float
        self.order_total -= float(price)

        return self.order_total
    

    def __repr__(self):
       return f"<Order: {self.order_id}>"
    
    
class ProductSchema(ma.Schema):

    class Meta:
        fields = ['prod_id', 'character_name', 'homeworld', 'price', 'quantity']



#instantiate our ProductSchema class so we can use them in our application
product_schema = ProductSchema()
products_schema = ProductSchema(many=True) 