from flask import Flask
from flask_smorest import Api
from services.fullname import blp as FullNameBlueprint
from services.braces import blp as BracesBlueprint

app = Flask(__name__)

app.config.from_pyfile("config.py")
api = Api(app)

api.register_blueprint(FullNameBlueprint)
api.register_blueprint(BracesBlueprint)
    
    