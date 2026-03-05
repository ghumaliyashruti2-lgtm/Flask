from flask import Blueprint, render_template, request, redirect, url_for
from .models import Post , Comment
from . import db
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask import flash

main = Blueprint("main", __name__)

# show blog detail 

@main.route("/")
@login_required
def home():
    # this show all user post its used when user have comment in post .
    posts = Post.query.all()
    '''# this show only user own post 
    posts = Post.query.filter_by(author=current_user).all()'''
    return render_template("index.html", posts=posts)

'''
# add blog detail 
@main.route("/add", methods=["GET","POST"])
@login_required
def add_post():

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        new_post = Post(title=title, content=content)

        db.session.add(new_post)
        db.session.commit()

        return redirect("/")

    return render_template("add_post.html")

# delete blog 
@main.route("/delete/<int:id>")
@login_required
def delete_post(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/")

# edit blog 
@main.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit_post(id):

    post = Post.query.get_or_404(id)

    if request.method == "POST":

        post.title = request.form["title"]
        post.content = request.form["content"]

        db.session.commit()

        return redirect("/")

    return render_template("edit_post.html", post=post)'''

# Register

@main.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists"
        
        # store password in has formate
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# Login 

@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Find user in database
        user = User.query.filter_by(username=username).first()

        # Check username exists AND password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.home"))

        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")

# Logout 

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

# add own post 
@main.route("/add", methods=["GET","POST"])
@login_required
def add_post():

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        new_post = Post(
            title=title,
            content=content,
            author=current_user
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect("/")

    return render_template("add_post.html")

# edit own post 
@main.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit_post(id):

    post = Post.query.get_or_404(id)

    # 🚨 IMPORTANT CHECK
    if post.author != current_user:
        return "You are not allowed to edit this post!"

    if request.method == "POST":

        post.title = request.form["title"]
        post.content = request.form["content"]

        db.session.commit()

        return redirect("/")

    return render_template("edit_post.html", post=post)

# delete own post 
@main.route("/delete/<int:id>")
@login_required
def delete_post(id):

    post = Post.query.get_or_404(id)

    # 🚨 IMPORTANT CHECK
    if post.author != current_user:
        return "You are not allowed to delete this post!"

    db.session.delete(post)
    db.session.commit()

    return redirect("/")

# profile 
@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

# add and show comment 
@main.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def add_comment(post_id):

    text = request.form["comment"]

    new_comment = Comment(
        text=text,
        user_id=current_user.id,
        post_id=post_id
    )

    db.session.add(new_comment)
    db.session.commit()

    return redirect("/")

# delete comment 

@main.route("/delete-comment/<int:id>")
@login_required
def delete_comment(id):

    comment = Comment.query.get_or_404(id)

    # Only comment owner can delete
    if comment.author != current_user:
        return "You cannot delete this comment"

    db.session.delete(comment)
    db.session.commit()

    return redirect("/")

# edit own comment post 
@main.route("/edit-comment/<int:id>", methods=["GET","POST"])
@login_required
def edit_comment(id):

    comment = Comment.query.get_or_404(id)

    # 🚨 IMPORTANT CHECK
    if comment.author != current_user:
        return "You are not allowed to edit this comment!"

    if request.method == "POST":

        comment.content = request.form["content"]

        db.session.commit()

        return redirect("/")

    return render_template("edit_comment.html", comment=comment)
