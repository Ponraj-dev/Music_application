from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from .utils import encode_image_to_base64


db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "Musicsite"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)


    from .views import views
    from .auth import auth
    from .songs import songs_blueprint
    from .playlist import playlist_bp
    from .album import album_bp



    from .models import User,Song,Rating,Playlist,Album
     
    with app.app_context():
        create_database()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

   

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    @app.context_processor
    def inject_user_info():
        profile_image_base64 = None
        if current_user.is_authenticated and hasattr(current_user, "image"):
            profile_image_base64 = encode_image_to_base64(current_user.image)

        user_info = {
            "current_user": current_user,
            "current_user_profile_image": profile_image_base64,
        }
        return user_info
    
        
    app.register_blueprint(songs_blueprint)
    app.register_blueprint(playlist_bp)
    app.register_blueprint(album_bp)
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    

    return app


def create_database():
    if not path.exists(DB_NAME):
        db.create_all()
        print("Created Database !")
