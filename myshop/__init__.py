from flask import Flask
from config import Config
from .blueprints.site.routes import site
from flask_migrate import Migrate 
from .models import login_manager, db 
from .blueprints.auth.routes import auth
from flask_cors import CORS 
from flask_jwt_extended import JWTManager 
from .helpers import JSONEncoder 



app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)


login_manager.init_app(app)
login_manager.login_view = 'auth.sign_in' 
login_manager.login_message = "Hey you! Log in please!"
login_manager.login_message_category = 'warning'

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

app.register_blueprint(site)
app.register_blueprint(auth)


db.init_app(app)
migrate = Migrate(app, db)
app.json_encoder = JSONEncoder
cors = CORS(app)
