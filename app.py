from flask import Flask
from db import db
from resources.item import Item, ItemList
from models.item import ItemModel 
from dbforresource.user import User, UserRegister
from security import authenticate, identity
from flask_jwt import JWT
from flask_restful import Resource, Api
# password forr droplet = 2151Jade



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db.init_app(app)
app.secret_key = 'jose'
api=Api(app)

jwt = JWT(app, authenticate, identity)


@app.before_first_request
def create_all():
    db.create_all()

api.add_resource(Item,"/item/<string:name>")
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister, '/register')

if __name__=="__main__":
    app.run(debug=True)

