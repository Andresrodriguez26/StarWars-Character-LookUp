from flask import Blueprint, flash, redirect, render_template, request


# Internal import
from myshop.models import Product, Customer, Order, db
from myshop.forms import ProductForm



# Need to instantiate our Blueprint Class
site = Blueprint("site", __name__, template_folder="site_templates")


# Use site object to create our routes
@site.route("/")
def shop():

    # We need to query our database to grab all of our products to display
    allprods = Product.query.all() 
    allcustomers = Customer.query.all()
    allorders = Order.query.all()

    # Making our dictionary for our shop stats/info

    shop_stats = {

        'products' : len(allprods),
        'sales' : sum(order.order_total for order in allorders), 
        'customers' : len(allcustomers)
    }


                                                # Whats on left side is html, right side whats in our route
    return render_template("shop.html", shop=allprods, stats=shop_stats) # Looking inside our template_folder (site_templates) to find our shop.hmtl file


@site.route("/shop/create", methods=["GET", "POST"])
def create():

    # Instantiate our productform

    createform = ProductForm()

    if request.method == "POST" and createform.validate_on_submit():
        # Grab our data from our form
        name = createform.character_name.data
        price = createform.price.data
        quantity = createform.quantity.data

       #instantiate that class as an object passing in our arguments to replace our parameters 

        product = Product(price, quantity, name)

        db.session.add(product) # Adding our new instantiating object to our database
        db.session.commit()

        flash(f"You have succesfully spawned character {name}", category="success")
        return redirect("/")
    
    elif request.method == "POST":
        flash("We were unable to process your request", category="warning")
        return redirect("/shop/create")
    

    return render_template("create.html", form=createform )


@site.route("/shop/update/<id>", methods=["GET","POST"]) 
def update(id):

    
    product = Product.query.get(id) 
    updateform = ProductForm()

    if request.method == "POST" and updateform.validate_on_submit():

        product.name = updateform.name.data 
        product.price = updateform.price.data 
        product.quantity = updateform.quantity.data 

        
        db.session.commit()

        flash(f"You have successfully updated product {product.name}", category='success')
        return redirect('/')
    
    elif request.method == "POST":
        flash("We were unable to process your request", category="warning")
        return redirect("/")
    
    return render_template('update.html', form=updateform, product=product )


@site.route('/shop/delete/<id>')
def delete(id):

    #query our database to find that object we want to delete
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()

    return redirect('/')


