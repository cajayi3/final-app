from functools import wraps
from flask import request, jsonify, current_app
import decimal
from json import JSONEncoder
import jwt

def verify_token(token):
    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError:
        print("Invalid token")   
    return None

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):

        token = request.cookies.get('jwt_token')
        print("All cookies:", request.cookies)
        print("JWT token:", token)

        data = verify_token(token)
        print("Decoded JWT data:", data)
        if not data:
            print("Token decoded failed.")
            return jsonify({"message": "Token is invalid or expired"}), 401
        
        current_user_token = data['user_token']
        if not current_user_token:
            return jsonify({"message":"User not found."}), 404
        
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated

class JSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)