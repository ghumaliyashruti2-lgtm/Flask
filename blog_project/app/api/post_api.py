from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

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
@login_required
def create_post():

    data = request.get_json()

    result, status = create_post_service(data, current_user.id)

    return jsonify(result), status

@post_api.route("/posts/<int:post_id>", methods=["PUT"])
@login_required
def edit_post(post_id):

    data = request.get_json()

    result, status = edit_post_service(post_id, data, current_user.id)

    return jsonify(result), status

@post_api.route("/posts/<int:post_id>", methods=["DELETE"])
@login_required
def delete_post(post_id):

    result, status = delete_post_service(post_id, current_user.id)

    return jsonify(result), status