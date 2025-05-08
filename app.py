from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)

#product model
class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    cost_price=db.Column(db.Float, nullable=False)
    selling_price=db.Column(db.Float,nullable=True)

#creating a database
with app.app_context():
    db.create_all()

#get all products
@app.route('/products',methods=['GET'])
def get_products():
    products=Product.query.all()
    res=[]
    for p in products:
        res.append({'id':p.id,
                    'name':p.name,
                    'cost_price':p.cost_price,
                    'selling_price':p.selling_price
                    })
    return jsonify(res)
    

#adding a new product to the database
@app.route('/products',methods=['POST'])  #POST /products end point
def add_products():
    data=request.json
    new_product=Product(name=data['name'],
                        cost_price=data['cost_price'],
                        selling_price=data['selling_price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message':'Product added'}),201


if __name__=='__main__':
    app.run(debug=True)
