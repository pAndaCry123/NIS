from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:test@localhost:5432/postgres"

db = SQLAlchemy(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

from views import *
from models import *

db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':

    app.run(port=5000, debug=True)