from flask import Blueprint, render_template, request, redirect, url_for
from .models import Post , Comment, Like
from . import db
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask import flash
from sqlalchemy import or_
import random
from app import mail
from email.mime.text import MIMEText
import smtplib, re
from flask import session

main = Blueprint("main", __name__)
# show blog detail 

'''
# normal home page show 
@main.route("/")
@login_required
def home():
    # this show all user post its used when user have comment in post .
    # posts = Post.query.all()
    # this show only user own post 
    # posts = Post.query.filter_by(author=current_user).all()
    return render_template("index.html", posts=posts)
'''

'''
# pagination add but not work because we have only one page 
@login_required
@main.route("/")
@main.route("/page/<int:page>")
def home(page=1):

    posts = Post.query.order_by(Post.id.desc()).paginate(
        page=page,
        per_page=5
    )

    return render_template("index.html", posts=posts)
 '''
# pagination show per page only one post show 
@login_required
@main.route("/")
def home():

    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.id.desc()).paginate(
        page=page,
        per_page=1
    )

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

# email validation 

def valid_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    return False


# Register
import random
@main.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        print("USERNAME:", username)
        print("EMAIL:", email)
        print("PASSWORD:", password)

        if not valid_email(email):
            print("EMAIL INVALID")
            flash("Invalid Email")
            return redirect(url_for("main.register"))

        existing = User.query.filter_by(email=email).first()

        if existing:
            print("EMAIL EXISTS")
            flash("Email already exists")
            return redirect(url_for("main.register"))

        print("REGISTER SUCCESS")

        otp = str(random.randint(100000,999999))

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            otp=otp
        )

        db.session.add(user)
        db.session.commit()

        send_otp_email(email, otp)

        session["verify_email"] = email

        return redirect(url_for("main.verify"))

    return render_template("register.html")

# otp generate 

def generate_otp():
    return str(random.randint(100000,999999))

# otp send 
def send_otp_email(receiver, otp):

    sender = "ghumaliyashruti2@gmail.com"
    password = "wxtx wbvm ygri ffei" # APP PASSWORD

    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Email Verification OTP"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)

    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

# verify email 
@main.route("/verify", methods=["GET","POST"])
def verify():

    email = session.get("verify_email")

    if not email:
        flash("Session expired")
        return redirect(url_for("main.register"))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found")
        return redirect(url_for("main.register"))

    if request.method == "POST":

        otp = request.form.get("otp")

        if otp == user.otp:

            user.is_verified = True
            user.otp = None

            db.session.commit()

            flash("Email Verified Successfully")

            return redirect(url_for("main.login"))

        else:
            flash("Invalid OTP")

    return render_template("verify.html")

# Login 
@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            if not user.is_verified:
                flash("Please verify your email first")
                session["verify_email"] = user.email
                return redirect(url_for("main.verify"))

            login_user(user)
            return redirect(url_for("main.home"))

        else:
            flash("Invalid username or password")

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
@main.route("/user/<username>")
def user_profile(username):

    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(user_id=user.id).all()

    # show comments in profile page .. 
    comments = Comment.query.filter_by(user_id=user.id).all()
    
    # show like in profile page 
    likes = Like.query.filter_by(user_id=user.id).all()

   
    return render_template("profile.html", user=user, posts=posts , comments=comments , likes=likes)


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


@main.route("/like/<int:post_id>")
@login_required
def like_post(post_id):

    post = Post.query.get_or_404(post_id)

    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if like:
        db.session.delete(like)   # unlike
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)

    db.session.commit()

    return redirect("/")

# search content 
@main.route("/search")
def search():

    query = request.args.get("query")

    # 1️⃣ search in posts
    matched_posts = Post.query.filter(
        or_(
            Post.title.ilike(f"%{query}%"),
            Post.content.ilike(f"%{query}%")
        )
    ).all()

    # 2️⃣ search in comments
    matched_comments = Comment.query.filter(
        Comment.text.ilike(f"%{query}%")
    ).all()

    return render_template(
        "search.html",
        posts=matched_posts,
        comments=matched_comments,
        query=query
    )