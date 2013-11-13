import json

from flask import Flask, jsonify, Markup, render_template, request

from salvavida.database import db_session, init_db
from salvavida.svmodels import Feed

app = Flask(__name__)

@app.route("/")
def index():
    feeds = [i.serialize for i in Feed.query.filter(Feed.tag=='sos').all()]
    return render_template('map.html', feeds=Markup(feeds))

@app.route("/rescue", methods=["POST", "GET"])
@app.route("/sos", methods=["POST", "GET"])
def sos():
    return jsonify(json.loads(request.data))

if __name__ == '__main__':
    app.debug = True
    app.run()
