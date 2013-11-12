import json

from flask import Flask, jsonify, Markup, render_template

from salvavida.database import db_session, init_db
from salvavida.svmodels import Feed

app = Flask(__name__)

@app.route("/")
def index():
    feeds = [i.serialize for i in Feed.query.all()]
    return render_template('map.html', feeds=Markup(feeds))

if __name__ == '__main__':
    app.debug = True
    app.run()
