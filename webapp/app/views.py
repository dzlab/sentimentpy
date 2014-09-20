__author__ = 'dzlab'

from app import app
from flask import render_template, flash, redirect

from core.inout.mongodb import MongoDb


@app.route("/")
@app.route('/comments')
def comments():
    db = MongoDb()
    comments = db.comments.find()
    return render_template("comments.html", title='Home', comments=comments)