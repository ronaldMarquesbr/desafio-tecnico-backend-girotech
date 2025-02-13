from flask import Blueprint, jsonify

hello_bp = Blueprint("hello_world", __name__)


@hello_bp.route("/hello", methods=["GET"])
def hello_world():
    return jsonify({"hello": "world"})
