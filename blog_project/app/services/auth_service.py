from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from flask import session

from app.repositories.user_repo import (
    get_user_by_email,
    get_user_by_username,
    save_user,
    update_user
)

from app.utils.otp import generate_otp
from app.utils.email_verify import send_otp_email
from app.models.user_model import User


# ====================
# REGISTER 
# ====================
def register_user(data):

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return {"error": "Invalid details"}, 400

    if get_user_by_email(email):
        return {"error": "Email already exists"}, 400

    if get_user_by_username(username):
        return {"error": "Username already exists"}, 400

    otp = generate_otp()
    hashed_password = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password=hashed_password,
        otp=otp
    )

    save_user(user)

    send_otp_email(email, otp)

    return {"message": "User registered. Verify OTP"}, 200

# ================
# VERIFY EMAIL
# ================
def verify_email(data):

    email = data.get("email")
    otp = data.get("otp")

    user = get_user_by_email(email)

    if not user:
        return {"error": "User not found"}, 404

    if otp != user.otp:
        return {"error": "Invalid OTP"}, 400

    user.is_verified = True
    user.otp = None

    update_user()

    return {"message": "Email verified successfully"}, 200

 
# ==================
# LOGIN 
# ===================
def login_user_service(data):

    username = data.get("username")
    password = data.get("password")

    user = get_user_by_username(username)

    if not user:
        return {"error": "User not found"}, 404

    if not check_password_hash(user.password, password):
        return {"error": "Invalid password"}, 401

    if not user.is_verified:
        return {"error": "Email not verified"}, 403

    login_user(user)

    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    }, 200
    
# ==================
# FORGOT PASSWORD 
# ===================    
def forgot_password(data):

    email = data.get("email")

    user = get_user_by_email(email)

    if not user:
        return {"error": "Email not registered"}, 404

    otp = generate_otp()

    user.otp = otp
    update_user()

    send_otp_email(email, otp)

    session["reset_email"] = email

    return {"message": "OTP sent to email"}, 200
    
# ==================
# VERIFY RESET OTP 
# ==================    
def verify_reset_otp(data):

    otp = data.get("otp")

    email = session.get("reset_email")

    if not email:
        return {"error": "Session expired"}, 400

    user = get_user_by_email(email)

    if otp != user.otp:
        return {"error": "Invalid OTP"}, 400

    session["reset_verified"] = True

    return {"message": "OTP verified"}, 200

# =================
# RESET PASSWORD 
# =================    
def reset_password(data):

    password = data.get("password")

    if not session.get("reset_verified"):
        return {"error": "OTP not verified"}, 403

    email = session.get("reset_email")

    user = get_user_by_email(email)

    user.password = generate_password_hash(password)
    user.otp = None

    update_user()

    session.pop("reset_email", None)
    session.pop("reset_verified", None)

    return {"message": "Password reset successfully"}, 200

# ==================
# LOGOUT 
# ==================    
def logout_user_service():

    logout_user()

    return {"message": "Logged out successfully"}, 200