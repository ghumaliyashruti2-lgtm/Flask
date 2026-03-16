from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from ..services.like_service import toggle_like_service

like_api = Blueprint("like_api", __name__)

@like_api.route("/like/<int:post_id>", methods=["POST"])
@login_required
def like_post(post_id):

    result, status = toggle_like_service(
        post_id,
        current_user.id
    )

    return jsonify(result), status