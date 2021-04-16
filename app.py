from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import List, TypedDict
import traceback

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test2.db'
db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    played_at = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    player_1_code = db.Column(db.String(80), nullable=False)
    player_1_character = db.Column(db.String(80), nullable=False)
    player_1_character_color = db.Column(db.String(80), nullable=False)
    player_2_code = db.Column(db.String(80), nullable=False)
    player_2_character = db.Column(db.String(80), nullable=False)
    player_2_character_color = db.Column(db.String(80), nullable=False)
    stage = db.Column(db.String(80), nullable=False)

    def __repr__(self) -> str:
        return '<Game %r>' % self.created_at


class UploadResponse(TypedDict):
    success: bool


@app.route('/upload', methods=['POST'])
def upload() -> UploadResponse:
    """
    a test with httpie
    http -v POST f00.pythonanywhere.com/upload duration=30 player_1_code=player1 player_2_code=player2 player_1_character=fox player_2_character=falco player_1_character_color=orange player_2_character_color=blue stage=Dreamland
    """
    try:
        post_data = request.json
        game = Game(played_at=datetime.now(),
            duration=post_data['duration'],
            player_1_code=post_data['player_1_code'],
            player_1_character=post_data['player_1_character'],
            player_1_character_color=post_data['player_1_character_color'],
            player_2_code=post_data['player_2_code'],
            player_2_character=post_data['player_2_character'],
            player_2_character_color=post_data['player_2_character_color'],
            stage=post_data['stage'])
        db.session.add(game)
        db.session.commit()
    except Exception:
        return {'success': False, 'error': traceback.format_exc()}
    return {'success': True}


class GamesResponse(TypedDict):
    games: List


@app.route('/games', methods=['GET'])
def games() -> GamesResponse:
    games = Game.query.all()
    return {'games': [game.id for game in games]}
