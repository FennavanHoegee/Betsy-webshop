# Models go here



import datetime

from peewee import *








db = SqliteDatabase('Betsy_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id= AutoField(unique=True)
    name = TextField()
    adress=CharField()
    billing_info=CharField()


class Product(BaseModel):
    product_id=AutoField(unique=True)
    product_name = TextField()
    description= CharField()
    price_unit= DecimalField(decimal_places=2, auto_round=True)
    quantity_in_stock= IntegerField()





class Transaction(BaseModel):
    transaction_id=AutoField(unique=True)
    payment_date= DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref='transactions')

class Product_User(BaseModel):
    pu_id=AutoField(unique=True)
    user= ForeignKeyField(User, backref='products_users')
    product_id=ForeignKeyField(Product, backref='products_users')
    quantity= IntegerField()

class Tag(BaseModel):
    tag_id=AutoField(unique=True)
    tag= CharField()

class ProductTags(BaseModel):
    product_id=ForeignKeyField(Product, backref='producttag')
    tag=ForeignKeyField(Tag, backref='producttag')


db.connect()
db.create_tables([User, Product, Product_User, Transaction, Tag, ProductTags])








