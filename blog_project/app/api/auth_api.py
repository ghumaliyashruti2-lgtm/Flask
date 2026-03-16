from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt
from ..extensions import jwt_blacklist
from app.services.auth_service import (
    register_user,
    verify_email,
    login_user_service,
    forgot_password,
    verify_reset_otp,
    reset_password,
    logout_user_service
)

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    result, status = register_user(data)

    return jsonify(result), status

@auth_api.route("/verify", methods=["POST"])
def verify():

    data = request.get_json()

    result, status = verify_email(data)

    return jsonify(result), status

@auth_api.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    result, status = login_user_service(data)

    return jsonify(result), status

@auth_api.route("/forgot-password", methods=["POST"])
def forgot():

    data = request.get_json()

    result, status = forgot_password(data)

    return jsonify(result), status

@auth_api.route("/verify-reset-otp", methods=["POST"])
def verify_reset():

    data = request.get_json()

    result, status = verify_reset_otp(data)

    return jsonify(result), status

@auth_api.route("/reset-password", methods=["POST"])
def reset():

    data = request.get_json()

    result, status = reset_password(data)

    return jsonify(result), status
from flask_login import login_required

@auth_api.route("/logout")
@jwt_required()
def logout():

    jti = get_jwt()["jti"]
    jwt_blacklist.add(jti)

    return jsonify({"message": "Logout successful"}), 200