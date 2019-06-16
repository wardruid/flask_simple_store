from flask import Blueprint, jsonify
from flask_restful import Api
from store.extensions import jwt_manager

from store.api.resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from store.api.resources.item import Item, ItemList
from store.api.resources.store import Store, StoreList
from store.api.blacklist import BLACKLIST

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


@jwt_manager.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # Instead of hard-coding you should read from config file or a database
        return {'is_admin': True}
    return {'is_admin': False}


@jwt_manager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt_manager.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt_manager.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt_manager.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does  not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt_manager.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt_manager.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
