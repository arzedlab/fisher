from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real.db'

app.config['SECRET_KEY'] = 'secret-key-goes-here'

db = SQLAlchemy(app)
def create_app():
    db.init_app(app)
    from models import URL 

from routes import *
db.create_all(create_app())
if __name__ == '__main__':
    app.run(debug=True)