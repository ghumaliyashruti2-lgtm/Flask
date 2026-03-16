from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

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
@login_required
def upload_profile_pic():

    file = request.files.get("profile_pic")

    result, status = upload_profile_picture_service(file, current_user)

    return jsonify(result), status

@profile_api.route("/delete-profile-image", methods=["DELETE"])
@login_required
def delete_profile_image():

    result, status = delete_profile_picture_service(current_user)

    return jsonify(result), status
