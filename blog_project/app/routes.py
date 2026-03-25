from flask import Blueprint, render_template, request, redirect, url_for
from app.models.user_model import User
from app.models.like_model import Like
from app.models.post_model import Post
from app.models.comment_model import Comment
from app.models.notification_model import Notification
from app.services.notification_service import create_notification
from . import db
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from flask import flash
from sqlalchemy import or_
import random
from app import mail
from email.mime.text import MIMEText
import smtplib, re
from flask import session
import os
from flask import current_app
from werkzeug.utils import secure_filename

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
'''

'''
# delete blog 
@main.route("/delete/<int:id>")
@login_required
def delete_post(id):

    post = Post.query.get_or_404(id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/")
'''

'''
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
'''

# ====================
# REGISTER 
# ====================

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

        otp = str(random.randint(100000,999999)) # otp generate 

        hashed_password = generate_password_hash(password) # conver password into hash 

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            otp=otp
        ) # store in database otp is (temparary)

        db.session.add(user)
        db.session.commit()
        # permenanat store user 
        send_otp_email(email, otp)
        # call send otp email function with parameter user email and otp 

        session["verify_email"] = email
        # store email in session 
        return redirect(url_for("main.verify"))
        # rediret page verify 

    return render_template("register.html")

# ==================
# EMAIL VALIDATION 
# ================== 

def valid_email(email):

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True
    return False

# ===============
# OTP GENERATE 
# ===============

def generate_otp():
    return str(random.randint(100000,999999)) 
    # generate otp 

# ================
# OTP SEDN 
# ================
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

# ================
# VERIFY EMAIL
# ================

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

# ==================
# LOGIN 
# ===================

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

# =================
# FORGOT PASSWORD
# =================

@main.route("/forgot-password", methods=["GET","POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get("email")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not registered")
            return redirect(url_for("main.forgot_password"))

        otp = str(random.randint(100000,999999))

        user.otp = otp
        db.session.commit()

        send_otp_email(email, otp)

        session["reset_email"] = email

        flash("OTP sent to your email")

        return redirect(url_for("main.verify_reset_otp"))

    return render_template("forgot_password.html")

# =============
# RESET OTP
# =============

@main.route("/verify-reset-otp", methods=["GET","POST"])
def verify_reset_otp():

    email = session.get("reset_email")

    if not email:
        flash("Session expired")
        return redirect(url_for("main.forgot_password"))

    user = User.query.filter_by(email=email).first()

    if request.method == "POST":

        otp = request.form.get("otp")

        if otp == user.otp:

            session["reset_verified"] = True
            flash("OTP Verified")

            return redirect(url_for("main.reset_password"))

        else:
            flash("Invalid OTP")

    return render_template("verify_reset_otp.html")

# =================
# RESET PASSWORD
# =================

@main.route("/reset-password", methods=["GET","POST"])
def reset_password():

    # get user email from session 
    email = session.get("reset_email")

    # when session expired its open forgot password page 
    if not email:
        return redirect(url_for("main.forgot_password"))

    # when session not expired  
    if request.method == "POST":

        # get new password 
        password = request.form.get("password")

        # check user email with athorised email
        user = User.query.filter_by(email=email).first()

        # password convert into hashpassword 
        hashed_password = generate_password_hash(password)

        # set user new password replace with old 
        user.password = hashed_password
        user.otp = None

        db.session.commit()

        # remove session data 
        session.pop("reset_email", None)
        session.pop("reset_verified", None)

        flash("Password reset successfully")

        return redirect(url_for("main.login"))

    return render_template("reset_password.html")

# ==================
# LOGOUT 
# ==================

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

# image extention 

ALLOWED_EXTENSIONS = {"png","jpg","jpeg","gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS


# ===========================================   
# PER PAGE ONE POST FOR PAGINATION  
# =========================================== 

'''@login_required
@main.route("/")
def home():

    page = request.args.get('page', 1, type=int)

    posts = Post.query.order_by(Post.id.desc()).paginate(
        page=page,
        per_page=1
    )

    return render_template("index.html", posts=posts)'''

# =======================
#  ALL POST IN ONE PAGE 
# =======================

@main.route("/")
@login_required
def home():
    # this show all user post its used when user have comment in post .
    posts = Post.query.order_by(Post.created_at.desc()).all()
    
    notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).limit(5).all()

    unread_count = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).count()
    # this show only user own post 
    # posts = Post.query.filter_by(author=current_user).all()
    return render_template("index.html", posts=posts, notifications=notifications,
        unread_count=unread_count)

# ===============
# ADD  POST 
# ===============
@main.route("/add", methods=["GET", "POST"])
@login_required
def add_post():

    if request.method == "POST":

        title = request.form.get("title")
        content = request.form.get("content")

        # get image file 
        file = request.files.get("image")
        filename = None

        # when file upload and not empty 
        if file and file.filename != "":
            filename = secure_filename(file.filename) # secure file from hacking 

            # get full folder path 
            upload_folder = os.path.join(
                current_app.root_path,
                "static/images/post_images"
            )

            # create folder if not exist
            os.makedirs(upload_folder, exist_ok=True)

            # full path folder + file 
            filepath = os.path.join(upload_folder, filename)

            file.save(filepath)

        post = Post(
            title=title,
            content=content,
            image=filename,
            user_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        flash("Post created successfully", "success")
        return redirect(url_for("main.home"))

    return render_template("add_post.html")


# =================
# EDIT  POST 
# =================

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

# =================
# DELETE  POST 
# =================

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

# ====================
# PROFILE 
# ====================

@main.route("/user/<username>")
def user_profile(username):

    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(user_id=user.id)\
        .order_by(Post.created_at.desc())\
        .all()

    # show comments in profile page .. 
    comments = Comment.query.filter_by(user_id=user.id).all()
    
    # show like in profile page 
    likes = Like.query.filter_by(user_id=user.id).all()

   
    return render_template("profile.html", user=user, posts=posts , comments=comments , likes=likes)

# ==========================
# UPLOAD PROFILE PICTURE 
# ==========================

@main.route("/upload-profile-pic", methods=["POST"])
@login_required
def upload_profile_pic():

    # get profile img
    file = request.files.get("profile_pic")

    # when user upload file 
    if file:

        filename = secure_filename(file.filename)

        # stored here user profile images 
        upload_folder = os.path.join(
            current_app.root_path,
            "static/images/profile_picture"
        )

        # when folder not exit 
        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(upload_folder, filename)

        file.save(filepath)

        # stored image in user field 
        current_user.profile_pic = filename
        db.session.commit()

        flash("Profile picture updated!")

    return redirect(url_for("main.user_profile", username=current_user.username))

# =========================
# DELETE PROFILE IMAGE 
# =========================

@main.route("/delete-profile-image", methods=["POST"])
@login_required
def delete_profile_image():

    if current_user.profile_pic != "default_profile.png":

        image_path = os.path.join(
            current_app.root_path,
            "static/images/profile_picture",
            current_user.profile_pic
        )

        if os.path.exists(image_path):
            os.remove(image_path)

        current_user.profile_pic = "default_profile.png"
        db.session.commit()

    flash("Profile image removed successfully", "success")

    return redirect(url_for("main.user_profile", username=current_user.username))


# ===========================
# LIKE POST 
# ==========================

@main.route("/like/<int:post_id>")
@login_required
def like_post(post_id):

    post = Post.query.get_or_404(post_id)

    like = Like.query.filter_by(
        user_id=current_user.id,
        post_id=post_id
    ).first()

    if like:
        db.session.delete(like)
        db.session.commit()
        return redirect("/")

    # ✅ Create like
    new_like = Like(
        user_id=current_user.id,
        post_id=post_id
    )
    db.session.add(new_like)

    # ✅ CREATE NOTIFICATION (same as API)
    if post.user_id != current_user.id:
        create_notification(
            user_id=post.user_id,
            sender_id=current_user.id,
            type="like",
            post_id=post_id
        )

    db.session.commit()

    return redirect("/")

# ========================
# SEARCH CONTENT  
# ========================

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
    

# ======================
# ADD AND SHOW COMMENT  
# =======================

@main.route("/comment/<int:post_id>", methods=["POST"])
@login_required
def add_comment(post_id):

    post = Post.query.get_or_404(post_id)
    text = request.form.get("comment")

    if not text:
        flash("Comment cannot be empty")
        return redirect(request.referrer)

    target_user_id = request.form.get("target_user_id")

    # 🔥 IMPORTANT FIX
    if target_user_id:
        target_user_id = int(target_user_id)
    else:
        # if no target → send to post owner
        target_user_id = post.user_id

    comment = Comment(
        text=text,
        user_id=current_user.id,
        post_id=post_id,
        target_user_id=target_user_id
    )

    db.session.add(comment)
    db.session.commit()

    # ✅ CREATE NOTIFICATION (same as API)
    if target_user_id != current_user.id:
        create_notification(
            user_id=target_user_id,
            sender_id=current_user.id,
            type="comment",
            post_id=post_id,
            comment_id=comment.id
        )

    return redirect("/")


# =====================
# REPLY COMMENT 
# ====================
@main.route("/reply/<int:post_id>", methods=["POST"])
@login_required
def reply_comment(post_id):

    text = request.form.get("text")
    parent_id = request.form.get("parent_id")

    parent = Comment.query.get_or_404(int(parent_id))

    receiver_id = parent.user_id

    comment = Comment(
        text=text,
        user_id=current_user.id,
        post_id=post_id,
        parent_id=parent.id,
        target_user_id=receiver_id
    )

    db.session.add(comment)
    db.session.commit()

    # ✅ MARK OLD NOTIFICATIONS AS READ
    Notification.query.filter_by(
        user_id=current_user.id,
        comment_id=parent.id,
        is_read=False
    ).update({"is_read": True})

    # ✅ CREATE NEW NOTIFICATION
    if receiver_id != current_user.id:
        create_notification(
            user_id=receiver_id,
            sender_id=current_user.id,
            type="reply",
            post_id=post_id,
            comment_id=comment.id
        )

    db.session.commit()

    return redirect("/")

# =====================
# DELETE COMMENT 
# =====================

@main.route("/delete-comment/<int:id>")
@login_required
def delete_comment(id):

    comment = Comment.query.get_or_404(id)

    # Only comment owner can delete
    if comment.author != current_user:
        return "You cannot delete this comment"

    # 🔥 DELETE RELATED NOTIFICATIONS (SAFE WAY)
    notifications = Notification.query.filter_by(comment_id=id).all()

    for n in notifications:
        db.session.delete(n)

    # delete comment
    db.session.delete(comment)

    db.session.commit()

    return redirect("/")

# ==========================
# EDIT COMMENT
# =========================

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

    
# =================
# NOTIFICATION 
# ================    
@main.route("/notifications")
@login_required
def notifications():

    notifications = Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).order_by(Notification.created_at.desc()).all()

    # ✅ MARK ALL AS READ
    Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).update({"is_read": True})

    db.session.commit()

    unread_count = 0  # now all are read

    return render_template(
        "notification.html",
        notifications=notifications,
        unread_count=unread_count
    )
    
    
@main.route("/read-notification/<int:id>")
@login_required
def read_notification(id):

    notification = Notification.query.get_or_404(id)

    if notification.user_id != current_user.id:
        return "Unauthorized"

    notification.is_read = True
    db.session.commit()

    # redirect to correct page
    if notification.post_id:
        return redirect(url_for("main.comment", post_id=notification.post_id, user_id=notification.sender_id))

    return redirect("/")    


# =================
# comment 
# ================    
@main.route("/comments/<int:post_id>")
@login_required
def comments(post_id):
    post = Post.query.get_or_404(post_id)

    # Get unique users who commented
    user_ids = set()

    for c in post.comments:
        if c.user_id != post.user_id:
            user_ids.add(c.user_id)

    users = User.query.filter(User.id.in_(user_ids)).all()

    return render_template("comment_list.html", post=post, users=users)

@main.route("/comment/<int:post_id>/<int:user_id>")
@login_required
def comment(post_id, user_id):

    post = Post.query.get_or_404(post_id)

    comments = Comment.query.filter(
        Comment.post_id == post_id,
        (
            ((Comment.user_id == current_user.id) & (Comment.target_user_id == user_id)) |
            ((Comment.user_id == user_id) & (Comment.target_user_id == current_user.id))
        )
    ).order_by(Comment.id).all()
    
    user = User.query.get_or_404(user_id)
    
    return render_template("comment.html", comments=comments, post=post, user_id=user_id,user=user)

@main.app_context_processor
def inject_unread_count():
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(
            user_id=current_user.id,
            is_read=False
        ).count()
    else:
        unread_count = 0

    return dict(unread_count=unread_count)