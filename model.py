from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime


app = Flask(__name__)

team="prod"
if team=="prod":
   db_url="postgresql://kkigykptcnjeuv:cd3496324c7af31c7162f8fb3b56b2184a8931f54ce77d3af097f99faf724cb8@ec2-18-214-176-16.compute-1.amazonaws.com:5432/d7p1bnea36g76g"
else:
   db_url='postgresql:///dummydb'



app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

eng=create_engine(db_url)



class Categories(db.Model):
    id=db.Column('category_id',db.String(100),primary_key=True, default = lambda: str(uuid.uuid4()))
    category_name=db.Column(db.String(100))
    def __init__(self, category_name):
        self.category_name=category_name
class SubCategories(db.Model):
    id=db.Column('subcategory_id',db.String(100),primary_key=True, default = lambda: str(uuid.uuid4()))
    category_id=db.Column(db.String(100),db.ForeignKey('categories.category_id'))
    subcategory_name=db.Column(db.String(100))
    def __init__(self, category_name):
        self.category_name=category_name
        self.category_id=category_id
        self.subcategory_name=subcategory_name


class Products(db.Model):
   __tablename__ = 'products'
   id=db.Column('product_id',db.String(100),primary_key=True, default = lambda: str(uuid.uuid4()))
   category_id=db.Column(db.String(100),db.ForeignKey('categories.category_id'))
   subcategory_id=db.Column(db.String(100),db.ForeignKey('sub_categories.subcategory_id'))
   product_name=db.Column(db.String(100))
   price=db.Column(db.Integer)
   striked_price=db.Column(db.Integer)
   product_image=db.Column(db.String(500))
   product_date=db.Column(DateTime, default=datetime.datetime.utcnow())
def __init__(self, product_id,category_id,subcategory_id,product_name,price,striked_price,product_image,product_date):
   self.product_id=product_id
   self.category_id=category_id
   self.subcategory_id=subcategory_id
   self.product_name=product_name
   self.price=price
   self.striked_price=striked_price
   self.product_image=product_image
   self.product_date=product_date

# for creating users
class Users(db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   phone = db.Column(db.String(20))  
   email = db.Column(db.String(200),unique=True)
   password = db.Column(db.String(300))

def __init__(self, name, phone, email,password):
   self.name = name
   self.phone = phone
   self.email = email
   self.password = password

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key = True)
    email=db.Column(db.String(200),db.ForeignKey('users.email'))
    product_id=db.Column(db.String(100))
def __init__(self, email,product_id):
   self.email = email
   self.product_id= product_id




# eng.execute("CREATE TABLE Users(id SERIAL PRIMARY KEY, name VARCHAR(50),phone varchar(20), email varchar(50), password varchar(255));")



   







   







     






if db.create_all():
    print("Tbale was Created")

