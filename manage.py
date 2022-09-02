from apps.models import Users

def deploy():
    from apps import create_app
    from apps.database import db

    app = create_app()
    app.app_context().push()
    db.create_all()

def dummy():
    from werkzeug.security import generate_password_hash
    from apps import create_app
    from apps.database import db

    app = create_app()
    app.app_context().push()

    db.session.add(Users('admin', generate_password_hash('password')))
    db.session.commit()


if __name__ == '__main__':
    deploy()
    dummy()