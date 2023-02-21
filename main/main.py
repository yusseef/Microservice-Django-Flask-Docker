from flask import Flask, jsonify
from flask import abort
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import requests
from producer import publish
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/main'
CORS(app)

db = SQLAlchemy(app)

@dataclass
class Product(db.Model):
    id:int
    title:str
    image:str
    id = db.Column(db.Integer, primary_key=True, autoincrement = False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id:int
    user_id:int
    product_id:int
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name = 'user_product_unique')

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://localhost:8000/api/user')
    json_data = req.json()
    try:
        product_user = ProductUser(user_id = json_data['id'], product_id = id)
        db.session.add(product_user)
        db.session.commit()
    #event 
        publish('Product_likes', id)
    except:
        abort(400, 'you already liked this product')
    return jsonify({
        'message': 'success',
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')