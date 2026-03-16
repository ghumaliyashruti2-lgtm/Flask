from flask import Blueprint, request, jsonify

from ..services.search_service import search_service

search_api = Blueprint("search_api", __name__)

@search_api.route("/search")
def search():

    query = request.args.get("query", "").strip()

    result, status = search_service(query)

    return jsonify(result), status
