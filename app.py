"""Blogly application."""

import os

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Post


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///users')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "shhh"

connect_db(app)




# @app.get('/')
# def show_home_page():
#     """List of users, button to add user."""
#     posts = Post.query.order_by('created_at")all()' ) #.desc()
#     return render_template('home.html', posts=posts)


@app.get('/')
def show_home_page():
    """List of users, button to add user."""
    return redirect('/users')


@app.get('/users')
def show_all_users():
    """Show all users"""
    # get database, pass users to index.html
    users = User.query.all()
    # contains link to the add-user form.
    return render_template('index.html', users=users)


@app.get('/users/new')
def show_add_form():
    """Show an add form for users"""
    return render_template('add_user.html')


@app.post('/users/new')
def add_new_user():
    """Process the add form, adding a new user and going back to /users"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form['image_url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    flash('User added!')
    return redirect('/users')


@app.get('/users/<int:user_id>')
def show_user_details(user_id):
    """Show information about the given user.
    Give options for editing/deleting user info."""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


@app.get('/users/<int:user_id>/edit')
def show_edit_details(user_id):
    """Show the edit page for a user.
    Have a cancel and save button for the opened form.
    """
    user = User.query.get(user_id)
    return render_template('edit_user.html', user=user)


@app.post('/users/<int:user_id>/edit')
def edit_user_details(user_id):
    """Update user info with form's values"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    image_url = request.form['image_url'] or None

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    #Otherwise, redirect them to the users page
    if not first_name or not last_name:
        if not first_name:
            flash("You must enter a first name!")
        if not last_name:
            flash("You must enter a last name!")
        return render_template("edit_user.html", user=user)
    else:
        print("\n\n got here?")
        flash("User edited successfully!")
        return redirect('/users')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete the user and return to the user list (while confirming delete)"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    flash("User deleted sucessfully.")
    return redirect('/users')


@app.get('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """Show an add form for users"""
    user = User.query.get(user_id)
    return render_template('add_post.html', user=user)


@app.post('/users/<int:user_id>/posts/new')
def add_new_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""
    title = request.form['title']
    content = request.form.get['content']

    if not title or not content:
        if not title:
            flash('A title is needed')
        if not content:
            flash('Post content is needed')
        return redirect('/users/<int:user_id>/posts/new')

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    flash('Post added!')
    return redirect(f"/users/{user_id}")





@app.get('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post"""
    post = Post.query.get(post_id)
    return render_template('post_detail.html', post=post)


@app.get('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show edit post form and have cancel to return to user page"""
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)


@app.post('/posts/<int:post_id>/edit')
def edit_post_details(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get(post_id)
    post.title = title
    post.content = content

    db.session.commit()

    #Otherwise, redirect them to the posts page
    if not title or not content:
        if not title:
            flash('A title is needed')
        if not content:
            flash('Post content is needed')
        return redirect(f"/posts/{post_id}/edit")
    else:
        flash("Post edited successfully!")
        return redirect(f"/posts/{post_id}")


@app.post('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete the user and return to the user list (while confirming delete)"""
    post = Post.query.get(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()

    flash("Post deleted sucessfully.")
    return redirect(f'/users/{user_id}')