from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.post_service import (
    get_posts_service,
    create_post_service,
    edit_post_service,
    delete_post_service
)

post_api = Blueprint("post_api", __name__)

@post_api.route("/posts")
def get_posts():

    result, status = get_posts_service()

    return jsonify(result), status


@post_api.route("/posts", methods=["POST"])
@jwt_required()
def create_post():

    user_id = int(get_jwt_identity())

    data = request.form   # important for image upload
    file = request.files.get("image")

    result, status = create_post_service(data, file, user_id)
    print("FORM DATA:", request.form)
    print("FILES:", request.files)
    return jsonify(result), status


@post_api.route("/posts/<int:post_id>", methods=["PUT"])
@jwt_required()
def edit_post(post_id):

    user_id = int(get_jwt_identity())

    data = request.get_json()

    result, status = edit_post_service(post_id, data, user_id)

    return jsonify(result), status


@post_api.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):

    user_id = int(get_jwt_identity())

    result, status = delete_post_service(post_id, user_id)

    return jsonify(result), status