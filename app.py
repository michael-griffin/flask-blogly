"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///users')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "shhh"

connect_db(app)


# GET /
#Redirect to list of users. (We’ll fix this in a later step).
@app.get('/')
def show_home_page():
    """List of users, button to add user."""
    return redirect('/users')


# GET /users
# Show all users.
@app.get('/users')
def show_all_users():
    """Show all users"""
    #get database, pass users to index.html
    users = User.query.all()
    return render_template('index.html', users=users)
#     Have a link here to the add-user form.

# GET /users/new
#     Show an add form for users
@app.post('/users/new')
def show_add_form():
    """Show an add form for users"""
#     Make these links to view the detail page for the user.

# POST /users/new
#     Process the add form, adding a new user and going back to /users
@app.post('/users/new')
def add_new_user():
    """Process the add form, adding a new user and going back to /users"""

# GET /users/[user-id]
@app.get('/users/<int:user_id>')
def show_user_details(user_id):
    """"""
    user = User.query.get(user_id)
    return render_template('user_detail.html', user=user)
#     Show information about the given user.
#     Have a button to get to their edit page, and to delete the user.


# GET /users/[user-id]/edit
@app.get('/users/<int:user_id>/edit')
def show_edit_details(user_id):
    """"""
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)
#     Show the edit page for a user.
#     Have a cancel button that returns to the detail page for a user, and a save button that updates the user.


@app.post('/users/<int:user_id>/edit')
def add_edit_details(user_id):
    """"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form['image_url']

    image_url = image_url if image_url else None
    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.commit()


    #check if first/last name is None (problem)
    #reload page with past inputs,

    #Otherwise, redirect them to the users page
    if not first_name or not last_name:
        #flash message warning them.
        #add a spot for flash messages on edit_user.html
        if not first_name:
            flash("You must enter a first name!")
        if not last_name:
            flash("You must enter a last name!")
        return render_template("edit_user.html", user=user)
    else:

        return redirect('/users')

# POST /users/[user-id]/edit
# Process the edit form, returning the user to the /users page.


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """"""

# POST /users/[user-id]/delete
# Delete the user.