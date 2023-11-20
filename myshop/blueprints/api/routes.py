from flask import Blueprint, request, jsonify 
from flask_jwt_extended import create_access_token, jwt_required 
from myshop.models import Customer, Product, ProdOrder, Order, db, product_schema, products_schema 


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/token', methods = ['GET', 'POST'])
def token():

    data = request.json()
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id) #just needs a unique identifier 
        return {
            'status': 200,
            'access_token': access_token
        }
    else:
        return {
            'status' : 400,
            'message' : 'Missing Client Id. Try Again.'
        }


@api.route('/shop')
@jwt_required()
def get_shop():

    #this is a list of objects
    allprods = Product.query.all()

    #since we cant send a list of objects through api calls we need to change them into dictionaries/jsonify them
    response = products_schema.dump(allprods) #loop through allprods list of objects and change objects into dictionarys
    return jsonify(response)


@api.route('/order/<cust_id>', methods = ['POST']) #CREATE is usually paired with a POST method 
@jwt_required()
def create_order(cust_id):

    data =  request.json

    customer_order = data['order'] #going to be a list of order dictionaries with prod_id, quantity, price 

    customer = Customer.query.filter(Customer.cust_id == cust_id).first() #searching the database for that customer
    if not customer: #if we dont have a customer, this is their first order and lets add them in the database
        customer = Customer(cust_id)
        db.session.add(customer)

    order = Order()
    db.session.add(order)

    for product in customer_order:

        #def __init__(self, prod_id, quantity, price, order_id, cust_id):

        prodorder = ProdOrder(product['prod_id'], product['quantity'], product['price'], order.order_id, customer.cust_id )
        db.session.add(prodorder)

        order.increment_ordertotal(prodorder.price)

        current_product = Product.query.get(product['prod_id'])
        #need to decrement the total quantitty available based on how much the customer bought
        current_product.decrement_quantity(product['quantity'])

    db.session.commit()

    return {
        'status' : 200,
        'message' : 'New Order was Created.'
    }


@api.route('/order/update/<order_id>', methods = ['PUT']) #whenever we are updating we using PUT
@jwt_required()
def update_order(order_id):

    data = request.json
    new_quantity = int(data['quantity'])
    prod_id = data['prod_id']



    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)



    prodorder.set_price(product.price, new_quantity)


    diff = abs(new_quantity - prodorder.quantity)


    if prodorder.quantity > new_quantity: 
        product.increment_quantity(diff) #we are putting some products back
        order.decrement_ordertotal(prodorder.price) #our order total is less $ now 

    elif prodorder.quantity < new_quantity:
        product.decrement_quantity(diff) #we are taking more quantity aaway
        order.increment_ordertotal(prodorder.price) #our order total is more $ now 

    prodorder.update_quantity(new_quantity)

    db.session.commit()

    return {
        'status': 200,
        'messagae': 'Order was Updated Successfully'
    }




@api.route('/order/delete/<order_id>', methods = ['DELETE'])
@jwt_required()
def delete_order(order_id):

    data = request.json
    prod_id = data['prod_id']


    prodorder = ProdOrder.query.filter(ProdOrder.order_id == order_id, ProdOrder.prod_id == prod_id).first()
    order = Order.query.get(order_id)
    product = Product.query.get(prod_id)


    order.decrement_ordertotal(prodorder.price) #less $ because deleted a product from our order
    product.increment_quantity(prodorder.quantity) #getting back some total quantity available to sell 

    db.session.delete(prodorder)
    db.session.commit()

    return {
        'status' : 200,
        'message': 'Order was Deleted Successfully'
    }