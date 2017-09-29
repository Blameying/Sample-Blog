from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import bcrypt
from flask_bootstrap import Bootstrap

app=Flask(__name__)
app.config.from_object('config')
db=SQLAlchemy(app)
bcrypt.init_app(app)
bootstrap = Bootstrap(app)



from app import views
