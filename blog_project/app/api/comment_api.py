from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.comment_service import (
    add_comment,
    reply_comment,
    get_post_comments,
    edit_comment,
    remove_comment,
    get_all_comments_service
)

comment_api = Blueprint("comment_api", __name__)

@comment_api.route("/comment", methods=["POST"])
@jwt_required()
def create_comment():

    user_id = int(get_jwt_identity())
    data = request.get_json()

    result, status = add_comment(data, user_id)

    return jsonify(result), status


@comment_api.route("/comment/reply", methods=["POST"])
@jwt_required()
def reply():

    user_id = int(get_jwt_identity())
    data = request.get_json()

    result, status = reply_comment(data, user_id)

    return jsonify(result), status


@comment_api.route("/comments/<int:post_id>")
def get_comments(post_id):

    result, status = get_post_comments(post_id)
    return jsonify(result), status


@comment_api.route("/comment/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update_comment(comment_id):

    user_id = int(get_jwt_identity())
    data = request.get_json()

    result, status = edit_comment(comment_id, data, user_id)

    return jsonify(result), status


@comment_api.route("/comment/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete(comment_id):

    user_id = int(get_jwt_identity())

    result, status = remove_comment(comment_id, user_id)

    return jsonify(result), status

@comment_api.route("/comments", methods=["GET"])
def get_all():

    result, status = get_all_comments_service()

    return jsonify(result), status