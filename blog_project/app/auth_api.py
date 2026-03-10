
from flask import Blueprint, request, jsonify
from . import db
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
import random
from email.mime.text import MIMEText
import smtplib, re
from flask import session

auth_api = Blueprint("auth_api", __name__)

# ====================
# REGISTER 
# ====================

@auth_api.route("/register", methods=["POST"])
def register_api():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON request"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "invalid details"}), 400

    if not valid_email(email):
        return jsonify({"error":"Invalid email"}),400
    
    existing_email = User.query.filter_by(email=email).first()
    
    if existing_email:
        return jsonify({"error":"Email already exists"}),400
    
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"error":"Username already exists"}),400

    otp = generate_otp()

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

    return jsonify({
        "message":"User registered. Verify OTP"
    })   
 
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

@auth_api.route("/verify", methods=["POST"])
def verify_api():

    data = request.get_json()

    email = data.get("email")
    otp = data.get("otp")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error":"User not found"}),404

    if otp != user.otp:
        return jsonify({"error":"Invalid OTP"}),400

    user.is_verified = True
    user.otp = None
    db.session.commit()

    return jsonify({
        "message":"Email verified successfully"
    })

 
# ==================
# LOGIN 
# ===================

@auth_api.route("/login", methods=["POST"])
def login_api():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error":"User not found"}),404

    if not check_password_hash(user.password, password):
        return jsonify({"error":"Invalid password"}),401

    if not user.is_verified:
        return jsonify({"error":"Email not verified"}),403

    login_user(user)

    return jsonify({
        "message":"Login successful",
        "user_id": user.id,
        "username": user.username
    })
    
# ==================
# FORGOT PASSWORD 
# ===================    

@auth_api.route("/forgot-password", methods=["POST"])
def forgot_password_api():

    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Email not registered"}), 404

    otp = str(random.randint(100000, 999999))

    user.otp = otp
    db.session.commit()

    send_otp_email(email, otp)

    session["reset_email"] = email

    return jsonify({
        "message": "OTP sent to email"
    })
    
# ==================
# VERIFY RESET OTP 
# ==================    
@auth_api.route("/verify-reset-otp", methods=["POST"])
def verify_reset_otp_api():

    data = request.get_json()
    otp = data.get("otp")

    email = session.get("reset_email")

    if not email:
        return jsonify({"error": "Session expired"}), 400

    user = User.query.filter_by(email=email).first()

    if otp == user.otp:

        session["reset_verified"] = True

        return jsonify({
            "message": "OTP verified"
        })

    else:
        return jsonify({"error": "Invalid OTP"}), 400
    
# =================
# RESET PASSWORD 
# =================    

@auth_api.route("/reset-password", methods=["POST"])
def reset_password_api():

    data = request.get_json()
    password = data.get("password")
    
    if not session.get("reset_verified"):
        return jsonify({"error":"OTP not verified"}),403

    email = session.get("reset_email")

    if not email:
        return jsonify({"error": "Session expired"}), 400

    user = User.query.filter_by(email=email).first()

    hashed_password = generate_password_hash(password)

    user.password = hashed_password
    user.otp = None

    db.session.commit()

    session.pop("reset_email", None)
    session.pop("reset_verified", None)

    return jsonify({
        "message": "Password reset successfully"
    })

# ==================
# LOGOUT 
# ==================    

@auth_api.route("/logout")
@login_required
def logout_api():

    logout_user()

    return jsonify({
        "message": "Logged out successfully"
    })
    
    