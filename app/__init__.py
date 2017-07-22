from flask import Flask
import os

app_ = Flask(__name__)
app_.config.from_object('config')


from app import views
