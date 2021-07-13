from flask import Blueprint, request, jsonify, make_response
from app import db
from dotenv import load_dotenv
from app.models.card import Card
from app.models.board import Board
import os

load_dotenv()

cards_bp = Blueprint('cards', __name__)
boards_bp = Blueprint('boards', __name__)

@boards_bp.route('/')
def root():
    return {
        "name":"mango-mania"
    }

@boards_bp.route('/boards', methods=["GET", "POST"], strict_slashes = False)
def handle_boards():
    if request.method == "GET":
        boards = Board.query.all()

        boards_response = []
        for board in boards:
            boards_response.append({
                "board_id": board.board_id,
                "title": board.title,
                "owner": board.owner,
            })
        return jsonify(boards_response)

    elif request.method == "POST":
        request_body = request.get_json()
        title = request_body.get("title")
        owner=request_body.get("owner")
        if "title" not in request_body or "owner" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
        new_board = Board(title=title,
                        owner=owner)
        db.session.add(new_board)
        db.session.commit()
        commited_board = {"board":
            {"board_id": new_board.board_id,
            "title": new_board.title,
            "owner": new_board.owner
        }}
        return jsonify(commited_board), 201     
        
@boards_bp.route("/boards/<board_id>", methods=["GET", "DELETE"])
def handle_board(board_id):
    board = Board.query.get_or_404(board_id)
    if request.method == "GET":
        selected_board = {"board":
        {"board_id": board.board_id,
        "title": board.title,
        "owner": board.owner,
        }}
        return jsonify(selected_board),200
    elif request.method == "DELETE":
        db.session.delete(board)
        db.session.commit()
        board_response_body = {"details": f'Board number {board.board_id} "{board.title}" successfully deleted'}
        return jsonify(board_response_body),200

@cards_bp.route("/boards/<board_id>/cards", methods=["GET","POST"])
def handle_cards(board_id):
    board = Board.query.get(board_id)

    if request.method == "GET":
        cards = board.cards
        cards_response = []
        for card in cards:
            cards_response.append({
            "id": card.card_id,
            "message": card.message,
            "votes": card.like_count,
        })
        return jsonify(cards_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "message" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        new_card = Card(message=request_body["message"], like_count=0, board_id=board.board_id)
        db.session.add(new_card)
        db.session.commit()
        commited_card = {"card": {
            "id": new_card.card_id,
            "message": new_card.message,
            "votes": new_card.like_count,
            "board_id": new_card.board_id
        }}
        return jsonify(commited_card), 201

@cards_bp.route("/<card_id>/votes", methods=["PATCH"])
def handle_card_like(card_id):
    card = Card.query.get_or_404(card_id)
    vote = request.args.get("like_count")
    card.like_count += int(vote)

    db.session.commit()
    response_body = {
        "card": {
            "id": card.card_id,
            "message": card.message,
            "like_count": card.like_count,
        }
    }
    return jsonify(response_body), 200

# @cards_bp.route("/<card_id>", methods=["DELETE"])
# def handle_card