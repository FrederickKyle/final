from flask import Blueprint, request, jsonify, render_template
from helpers import token_required 
from models import db, User, Sport, sport_schema, sports_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/anime')
def anime():
    return {'Naruto Uzamaki': '7th Hokage'}

@api.route('/sport', methods = ['POST'])
@token_required
def create_sport(current_user_token):
    name = request.json['name']
    equipment = request.json['equipment']
    type = request.json['type']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token}')

    sport = Sport(name, equipment, type, user_token=user_token)

    db.session.add(sport)
    db.session.commit()

    response = sport_schema.dump(sport)
    return jsonify(response)

@api.route('/sport', methods = ['GET'])
@token_required
def get_sport(current_user_token):
    a_user = current_user_token.token
    sport = Sport.query.filter_by(user_token = a_user).all()
    response = sports_schema.dump(sport)
    return jsonify(response)

@api.route('/sport/<id>', methods = ['GET'])
@token_required
def get_single_sport(current_user_token, id):
    sport = Sport.query.get(id)
    response = sport_schema.dump(sport)
    return jsonify(response)

@api.route('/sport/<id>', methods = ['POST', 'PUT'])
@token_required
def update_sport(current_user_token, id):
    sport = Sport.query.get(id)
    sport.name = request.json['name']
    sport.model = request.json['equipment']
    sport.type = request.json['type']
    sport.user_token = current_user_token.token

    db.session.commit()
    response = sport_schema.dump(sport)
    return jsonify(response)

@api.route('/sport/<id>', methods = ['DELETE'])
@token_required
def delete_sport(current_user_token, id):
    sport = Sport.query.get(id)
    db.session.delete(sport)
    db.session.commit()
    response = sport_schema.dump(sport)
    return jsonify(response)