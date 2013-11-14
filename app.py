import json

from datetime import datetime

from flask import Flask, jsonify, Markup, render_template, request
from pygeocoder import Geocoder

from salvavida.database import db_session
from salvavida.svmodels import Feed

app = Flask(__name__)

@app.route("/")
def index():
    feeds = [i.serialize for i in Feed.query.filter(Feed.state=='open').all()]
    return render_template('map.html', feeds=Markup(feeds))

@app.route("/sos", methods=["POST"])
def sos():
    data = json.loads(request.data)
    name = data.get('name').upper()
    lat = data.get('lat')
    lng = data.get('lng')
    description = data.get('description')
    feed = Feed.query.filter(Feed.name==name, Feed.lat==lat, Feed.lng==lng,
                             Feed.state=='open').first()
    result = None
    if not feed:
        try:
            address = Geocoder.reverse_geocode(float(lat), float(lng))[0]
            new_feed = Feed(name=name, lat=lat, lng=lng, address=address,
                description=description)
            db_session.add(new_feed)
            db_session.commit()
            result = {
                'id': new_feed.id,
                'lat': new_feed.lat,
                'lng': new_feed.lng,
                'createdAt':
                    new_feed.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'name': new_feed.name,
                'description': new_feed.description,
                'state': new_feed.state
            }
        except:
            result = { 'error_msg': 'DB Error' }
        finally:
            db_session.remove()
    else:
        result = {
            'error_msg': 'Entry exists.'
        }
    return jsonify(result)

@app.route("/rescue", methods=["POST"])
def rescue():
    data = json.loads(request.data)
    result = None
    try:
        id = int(data.get('id'))
        feed = Feed.query.filter(Feed.id==id).first()
        if feed:
            feed.state = 'closed'
            feed.last_modified = datetime.now()
            db_session.merge(feed)
            db_session.commit()
            result = {
                'id': feed.id,
                'lat': feed.lat,
                'lng': feed.lng,
                'lastModified': 
                    feed.last_modified.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'name': feed.name,
                'description': feed.description,
                'state': feed.state
            }
        else:
            result = { 'error_msg': 'Entry does not exist.' }
    except ValueError:
        result = { 'error_msg': 'Invalid ID format %s' % (data.get('id')) }
    except:
        result = { 'error_msg': 'Internal error.' }
    finally:
        db_session.remove()
    
    return jsonify(result)

@app.route("/rescues", methods=["GET"])
def rescues():
    ts = datetime.strptime(request.args.get('since'), '%Y-%m-%dT%H:%M:%SZ')
    feeds = Feed.query.filter(Feed.state=='closed',
                Feed.last_modified>=ts).all()
    result = []
    if feeds:
        for feed in feeds:
            result.append({
                'id': feed.id,
                'lat': feed.lat,
                'lng': feed.lng,
                'createdAt': feed.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'lastModified':
                    feed.last_modified.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'name': feed.name,
                'description': feed.description,
                'state': feed.state
            })
    response = {'results': result}
    return jsonify(response)

if __name__ == '__main__':
    app.debug = True
    app.run()
