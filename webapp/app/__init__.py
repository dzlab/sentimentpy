__author__ = 'dzlab'

from flask import Flask

app = Flask(__name__)
app.config.from_object('webapp.config')

from app import views