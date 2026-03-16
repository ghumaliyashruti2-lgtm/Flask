from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.services.comment_service import (
    add_comment,
    reply_comment,
    get_post_comments,
    edit_comment,
    remove_comment
)

comment_api = Blueprint("comment_api", __name__)

@comment_api.route("/comment", methods=["POST"])
@login_required
def create_comment():

    data = request.get_json()

    result, status = add_comment(data, current_user.id)

    return jsonify(result), status

@comment_api.route("/comment/reply", methods=["POST"])
@login_required
def reply():

    data = request.get_json()

    result, status = reply_comment(data, current_user.id)

    return jsonify(result), status

@comment_api.route("/comments/<int:post_id>")
def get_comments(post_id):

    result, status = get_post_comments(post_id)

    return jsonify(result), status

@comment_api.route("/comment/<int:comment_id>", methods=["PUT"])
@login_required
def update_comment(comment_id):

    data = request.get_json()

    result, status = edit_comment(comment_id, data, current_user.id)

    return jsonify(result), status

@comment_api.route("/comment/<int:comment_id>", methods=["DELETE"])
@login_required
def delete(comment_id):

    result, status = remove_comment(comment_id, current_user.id)

    return jsonify(result), status