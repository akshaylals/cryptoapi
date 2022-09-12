import os
from importlib import import_module

from cryptography.hazmat.primitives import serialization

from apps.config import CERTIFICATE_DIR


curves = [
    'SECP256R1',
    'SECP384R1',
    'SECP521R1',
    'SECP224R1',
    'SECP192R1',
    'SECP256K1',
    'BrainpoolP256R1',
    'BrainpoolP384R1',
    'BrainpoolP512R1',
    'SECT571K1',
    'SECT409K1',
    'SECT283K1',
    'SECT233K1',
    'SECT163K1',
    'SECT571R1',
    'SECT409R1',
    'SECT283R1',
    'SECT233R1',
    'SECT163R2',
]


def createRsa(filename, public_exponent, key_size):
    from cryptography.hazmat.primitives.asymmetric import rsa

    if os.path.exists(os.path.join(CERTIFICATE_DIR, filename)) or os.path.exists(os.path.join(CERTIFICATE_DIR, filename + '.pub')):
        return {'message': 'File already exists', 'status': 400}

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
    
    return {
        'message': 'success',
        'certificate': {
            'algorithm': 'RSA',
            'private_key_file': filename,
            'public_key_file': filename + '.pub',
            'public_exponent': public_exponent,
            'key_size': key_size
        },
        'status': 200
    }


def createEd25519(filename):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    
    if os.path.exists(os.path.join(CERTIFICATE_DIR, filename)) or os.path.exists(os.path.join(CERTIFICATE_DIR, filename + '.pub')):
        return {'message': 'File already exists', 'status': 400}

    private_key = Ed25519PrivateKey.generate()

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
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
    
    return {
        'message': 'success',
        'certificate': {
            'algorithm': 'Ed25519',
            'private_key_file': filename,
            'public_key_file': filename + '.pub'
        },
        'status': 200
    }


def createEd448(filename):
    from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
    
    if os.path.exists(os.path.join(CERTIFICATE_DIR, filename)) or os.path.exists(os.path.join(CERTIFICATE_DIR, filename + '.pub')):
        return {'message': 'File already exists', 'status': 400}

    private_key = Ed448PrivateKey.generate()

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
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
    
    return {
        'message': 'success',
        'certificate': {
            'algorithm': 'Ed448',
            'private_key_file': filename,
            'public_key_file': filename + '.pub'
        },
        'status': 200
    }


def createEC(filename, curve):
    from cryptography.hazmat.primitives.asymmetric.ec import generate_private_key
    
    if os.path.exists(os.path.join(CERTIFICATE_DIR, filename)) or os.path.exists(os.path.join(CERTIFICATE_DIR, filename + '.pub')):
        return {'message': 'File already exists', 'status': 400}

    if curve not in curves:
        return {'message': 'Invalid or Unsupported curve', 'curves': curves, 'status': 400}

    c = getattr(import_module('cryptography.hazmat.primitives.asymmetric.ec'), curve)
    private_key = generate_private_key(c)

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
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
    
    return {
        'message': 'success',
        'certificate': {
            'curve': curve,
            'private_key_file': filename,
            'public_key_file': filename + '.pub'
        },
        'status': 200
    }
