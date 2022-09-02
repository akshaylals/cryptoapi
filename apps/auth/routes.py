from flask import request, jsonify
from werkzeug.security import check_password_hash
import jwt

from . import bp
from apps.models import Users
from apps.config import Config

@bp.route('/login', methods=['POST']) 
def login_user():
   auth = request.authorization  
   if not auth or not auth.username or not auth.password: 
       return jsonify({'Authentication': 'login required"'}), 401
 
   user = Users.query.filter_by(username=auth.username).first()  
   if check_password_hash(user.password, auth.password):
       token = jwt.encode({'public_id' : user.public_id}, Config.SECRET_KEY, "HS256")
 
       return jsonify({'token' : token}), 200
 
   return jsonify({'Authentication': 'login required'}), 401