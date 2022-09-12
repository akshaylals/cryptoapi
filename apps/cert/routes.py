import os

from flask import request, jsonify, abort


from apps.auth.utils import token_required
from . import bp
from apps.config import CERTIFICATE_DIR
from .utils import createRsa, createEd25519, createEd448, createEC

@bp.route('/', methods=['GET'])
@token_required
def certificate_get(user):
    response = {}
    if request.args.get('public'):
        file = os.path.join(CERTIFICATE_DIR, request.args.get('public') + '.pub')
        print(file)
        if os.path.exists(file):
            with open(file, "rb") as f:
                key = f.read()
            response['public_key'] = key.decode()
        else:
            abort(404)

    if request.args.get('private'):
        file = os.path.join(CERTIFICATE_DIR, request.args.get('private'))
        if os.path.exists(file):
            with open(file, "rb") as f:
                key = f.read()
            response['private_key'] = key.decode()
        else:
            abort(404)
    
    if len(response) > 0:
        return jsonify(response), 200
    
    return jsonify({'message': 'specify public key or private key filename'}), 400

@bp.route('/', methods=['POST'])
@token_required
def certificate_post(user):
    algo = request.json.get('algorithm')
    filename = request.json.get('filename')

    if not filename:
        return jsonify({'message': 'filename not specified'}), 400
    
    if not algo:
        return jsonify({'message': 'algorithm not specified'}), 400

    match algo:
        case 'RSA':
            public_exponent = request.json.get('public_exponent', 65537)
            key_size = request.json.get('key_size', 2048)
            response = createRsa(filename, public_exponent, key_size)
        case 'Ed25519':
            response = createEd25519(filename)
            pass
        case 'Ed448':
            response = createEd448(filename)
            pass
        case 'ECC':
            curve = request.json.get('curve')
            if not curve:
                return jsonify({'message': 'elliptic curve not specified'}), 400
            response = createEC(filename, curve)
            pass
    
    s = response.pop('status')
    
    return jsonify(response), s

