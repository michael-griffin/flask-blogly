"""Blogly application."""

import os

from flask import Flask
from models import connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


# GET /
#Redirect to list of users. (We’ll fix this in a later step).
@app.get('/')
def show_home_page():
    """List of users, button to add user."""

# GET /users
# Show all users.
@app.get('/users')
def show_all_users():
    """Show all users"""
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
@app.get('/users/<int: user_id>')
def show_user_details(user_id):
#     Show information about the given user.
#     Have a button to get to their edit page, and to delete the user.


# GET /users/[user-id]/edit
@app.get('/users/<int: user_id>/edit')
def show_edit_details(user_id):
#     Show the edit page for a user.
#     Have a cancel button that returns to the detail page for a user, and a save button that updates the user.


@app.post('/users/<int: user_id>/edit')
def add_edit_details(user_id):
# POST /users/[user-id]/edit
# Process the edit form, returning the user to the /users page.


@app.post('/users/<int: user_id>/delete')
def delete_user(user_id):
# POST /users/[user-id]/delete
# Delete the user.