import os

from flask import request, jsonify, abort
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from . import bp
from apps.config import CERTIFICATE_DIR

@bp.route('/', methods=['GET'])
def certificate_get():
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
def certificate_post():
    filename = request.json.get('filename')
    public_exponent = request.json.get('public_exponent', 65537)
    key_size = request.json.get('key_size', 2048)

    if not filename:
        return jsonify({'message': 'filename not specified'}), 400

    if os.path.exists(os.path.join(CERTIFICATE_DIR, filename)) or os.path.exists(os.path.join(CERTIFICATE_DIR, filename + '.pub')):
        return jsonify({'message': 'File already exists'}), 400

    private_key = rsa.generate_private_key(
        public_exponent = public_exponent,
        key_size = key_size,
    )

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(os.path.join(CERTIFICATE_DIR, filename), "wb") as f:
        f.write(pem)
    
    public_key = private_key.public_key()

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(os.path.join(CERTIFICATE_DIR, filename + '.pub'), "wb") as f:
        f.write(pem)
    
    return jsonify({
        'message': 'success',
        'certificate': {
            'private_key_file': filename,
            'public_key_file': filename + '.pub',
            'public_exponent': public_exponent,
            'key_size': key_size
        }
    })

