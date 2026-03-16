from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.like_service import toggle_like_service

like_api = Blueprint("like_api", __name__)

@like_api.route("/like/<int:post_id>", methods=["POST"])
@jwt_required()
def like_post(post_id):

    user_id = int(get_jwt_identity())

    result, status = toggle_like_service(
        post_id,
        user_id =user_id
    )

    return jsonify(result), status