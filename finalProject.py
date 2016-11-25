from flask import Flask, render_template, redirect, request, url_for



restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},
{'name':'Taco Hut', 'id':'3'}]

items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, 
{'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},
{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},
{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},
{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'}]

item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

app = Flask(__name__)

@app.route('/')
@app.route('/restaurant/')
def showRestaurants(restaurants):
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])    
def newRestaurant(id):
	if request.method =='POST':
		newrestaurant = restaurant(name=request.form['name'])
		session.add(newrestaurant)
		session.commit()
	    return redirect(url_for('restaurants.html', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)



@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST']))
def editRestaurant(restaurants_id):
	editrestaurant = session.query(restaurants).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editrestaurant.name=request.form['name']
			session.add(editrestaurant)
			session.commit()
			return redirect(url_for('restaurants.html', restaurants_id=restaurant_id))
		else:
			return render_template('editrestaurant.html', restaurants_id=restaurant_id)



@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST']))	
def deleteRestaurant(restaurants_id):
	itemtodelete = session.query(restaurants).filter_by(id=restaurants.id))
	if request.method == 'POST':
		session.delete(itemtodelete)
		session.commit()
		return redirect(url_for('restaurants', id=restaurants.id))
	else:
		return render_template ("deleterestaurant.html")


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	restaurant = session.query(restaurants).filter_by(id=restaurants.id).one()
	items = session.query(items).filter_by(id=restaurant.id)
    return render_template('menu.html', restaurants=restaurant, items=items, restaurant_id=restaurant.id)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST']))
def newmenuitem(restaurant_id):
	if request.method =='POST':
		newItem = Items(name= request.form['name'], description = request.form['description'], price = request.form['price'],
		 course = request.form['course'], Entree = request.form['Entree'])
		session.add(newItem)
		session.commit()
		return redirect(url_for('newmenuitem.html', restaurant_id=restaurant.id))
	else:
		return render_template("newmenuitem.html", restaurant_id= restaurant.id)

	

@app.route('/restaurant/<int:restaurant_id>/menu/menu_id/edit', methods=['GET', 'POST']))
def editmenuitem(restaurant_id, menu_id):
	editedItem = session.query(Items).filter_by(menu_id=menu.id).one()
	if request.method =='POST':
		if request.form['name']:
			editedItem.name= request.form['name']
		if request.form['description']:
			editedItem.description= request.form['description']
		if request.form['price']:
			editedItem.price= request.form['price']
		if request.form['course']:
			editedItem.course= request.form['course']
		if request.form['Entree']:
			editedItem.Entree= request.form['Entree']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('restaurants', restaurant_id=restaurants_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurants.id, item_id = items.id, item = editedItem)



@app.route('/restaurant/<int:restaurant_id>/menu/menu_id/delete', methods=['GET', 'POST'])
def deletemenuitem(restaurant_id, menu_id):
	itemtodelete = session.query(Items).filter_by(menu_id=menu.id).one()
	if request.method == 'POST':
		session.delete(itemtodelete)
		session.commit()
		return redirect(url_for('restaurants', restaurant_id=restaurants.id))
	else:
		return render_template('deletemenuitem.html', item=itemtodelete)


if __name__=='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)	

	