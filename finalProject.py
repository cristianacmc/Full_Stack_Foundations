from flask import Flask, flash, render_template, redirect, request, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurant=restaurants)


@app.route('/')
@app.route('/restaurant/JSON')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(restaurants=[r.serialize for r in restaurants])


@app.route('/restaurant/new', methods=['GET', 'POST'])    
def newRestaurant():
	if request.method =='POST':
		newrestaurant = Restaurant(name=request.form['name'])
		session.add(newrestaurant)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newrestaurant.html')



@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	editrestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editrestaurant.name=request.form['name']
			flash ("Restaurant Successfully Edited")
			return redirect(url_for('showRestaurants'))
	else:
		return render_template('editrestaurant.html', restaurant=editrestaurant)



@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	itemtodelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(itemtodelete)
		session.commit()
		return redirect(url_for('showRestaurants'))
	else:
		return render_template ('deleterestaurant.html', restaurant=itemtodelete)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return render_template('menu.html', items=items, restaurant=restaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])    	
def newMenuItem(restaurant_id):
	if request.method =='POST':
		newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], 
						course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)		
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)
	
	


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editmenuitem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
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
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)



@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deletemenuitem(restaurant_id, menu_id):
	itemtodelete = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(itemtodelete)
		session.commit()
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deletemenuitem.html', item=itemtodelete)


if __name__=='__main__':
	app.secret_key='super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)	

	