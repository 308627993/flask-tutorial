from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

class Config(object):
    SECRET_KEY = '0ad5e132f08f5df90863aaa2715654f8'

class ProdConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    #SQLALCHEMY_ECHO = True # sqlalchemy 翻译sql查询语句



db = SQLAlchemy()
migrate = Migrate()
