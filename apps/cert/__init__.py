from flask import Blueprint

bp = Blueprint(
    'cert_bp', __name__,
    url_prefix='/certificate'
)