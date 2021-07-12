from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

card_bp = Blueprint('card_bp', __name__)
board_bp = Blueprint('board_bp', __name__)

@board_bp.route('/', methods=["GET"])
def root():
    return {"name":"soemthing"}