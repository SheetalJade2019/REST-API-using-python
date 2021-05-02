from flask_restful import Resource,reqparse
from models.item import ItemModel
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",type=float,required=True, help="It can not be empty")
    parser.add_argument("store_id",type=int,required=False, help="It can not be empty")

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message":"Item not found"},404

    def post(self, name):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(name):
            return {"message": f"Item with name {name} already exists."},400
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {"message":"Error occured while saving data to database"},500
        return item.json() , 201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {"message": f"Item with name {name} does not exists."},404
        try:
            item.delete_from_db()
            return {"message":"item deleted"},200
        except:
            return {"message":"Error while deleting data from database"},500
        
    def put(self,name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name,data['price'])
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        data = ItemModel.query.all()
        # print(type(data))
        itemlist = list(map(lambda x : x.json(),data))
        return {'items':itemlist}