from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.profile_service import (
    get_user_profile_service,
    upload_profile_picture_service,
    delete_profile_picture_service
)

profile_api = Blueprint("profile_api", __name__)

@profile_api.route("/user/<username>")
def user_profile(username):

    result, status = get_user_profile_service(username)

    return jsonify(result), status


@profile_api.route("/upload-profile-pic", methods=["POST"])
@jwt_required()
def upload_profile_pic():
    
    user_id = int(get_jwt_identity())

    file = request.files.get("profile_pic")

    result, status = upload_profile_picture_service(file, user_id)

    return jsonify(result), status

@profile_api.route("/delete-profile-image", methods=["DELETE"])
@jwt_required()
def delete_profile_image():
    
    user_id = int(get_jwt_identity())

    result, status = delete_profile_picture_service(user_id)

    return jsonify(result), status
