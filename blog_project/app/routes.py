from flask import Blueprint, render_template, request, redirect
from .models import Post
from . import db
from flask_login import login_user, logout_user, login_required
from .models import User

main = Blueprint("main", __name__)

# show blog detail 
@main.route("/")
def home():

    posts = Post.query.all()

    return render_template("index.html", posts=posts)

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

    return render_template("edit_post.html", post=post)

# Register

@main.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        new_user = User(username=username, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")

# Login 

@main.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            return redirect("/")

    return render_template("login.html")
