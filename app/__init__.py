from flask import Flask
import os

app_ = Flask(__name__)
app_.config.from_object('config')
app_.config.update(dict(
    DATABASE=os.path.join(app_.root_path, 'test2.db')
))
from app import views
