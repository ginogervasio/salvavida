import logging

import config

from datetime import datetime

from pygeocoder import Geocoder
from sqlalchemy.exc import DBAPIError, DisconnectionError
from twython import TwythonStreamer

from database import db_session, init_db
from svmodels import Feed

class SalvaVida():
    """ Main class. """

    def __init__(self):
        """ Constructor."""

        init_db()
        c = config.Config()
        self.config = c.cfg
        logging.basicConfig(filename=self.config.get('salvavida', 'logfile'),
            level=logging.DEBUG)
        self.stdin_path = '/dev/null'
        self.stdout_path = self.config.get('salvavida', 'logfile')
        self.stderr_path = self.config.get('salvavida', 'errfile')
        self.pidfile_path = self.config.get('salvavida', 'pidfile')
        self.pidfile_timeout = 5
        self.feed_tags = self.config.get('twitter', 'feed_tags')
        self.reply_tags = self.config.get('twitter', 'reply_tags')
        self.filter_tags = self.config.get('twitter', 'filter_tags')

    def run(self):
        """ Setup TwitterStreamer. """

        app_key = self.config.get('twitter', 'app_key')
        app_secret = self.config.get('twitter', 'app_secret')
        oauth_token = self.config.get('twitter', 'oauth_token')
        oauth_token_secret = self.config.get('twitter', 'oauth_token_secret')
        self.stream = TwitterStreamer(app_key, app_secret, oauth_token,
            oauth_token_secret)
        self.stream.set_tags(self.feed_tags, self.reply_tags)
        self.stream.statuses.filter(track=self.filter_tags)

class TwitterStreamer(TwythonStreamer):
    """ Salva Vida main class."""

    def set_tags(self, feed_tags, reply_tags):
        self.feed_tags = feed_tags
        self.reply_tags = reply_tags

    def get_feed(self, name, lat, lng, state='open'):
        return Feed.query.filter(Feed.name==name, Feed.lat==lat,
                    Feed.lng==lng, Feed.state==state).first()

    def on_success(self, data):
        if 'text' in data:
            try:
                (_, tag, name, address) = data['text'].split('\\', 4)
                result = Geocoder.geocode(address)
                (lat, lng) = result[0].coordinates
                formatted_address = result[0].formatted_address
                feed = self.get_feed(name.upper(), lat, lng)
                if feed:
                    # Filter dupes
                    logging.debug('Feed exists: %s' % (feed))
                    if tag.upper() in self.reply_tags.upper():
                        feed.state = 'closed'
                        feed.last_modified = datetime.now()
                        db_session.merge(feed)
                        db_session.commit()
                        logging.debug('Feed updated: %s' % (feed))
                else:
                    f = Feed(name=name.upper(),lat=lat,
                        lng=lng, address=formatted_address)
                    db_session.add(f)
                    db_session.commit()
                    logging.debug('Feed created: %s' % (f))
            except DisconnectionError as e:
                print e
                logging.error(e)
                db_session.remove()
                db_session.init()
            except ValueError as e:
                pass
            except (DBAPIError, Exception) as e:
                logging.error(e)
    

        # Want to disconnect after the first result?
        # self.disconnect()

    def on_error(self, status_code, data):
        logging.error(status_code, data)


if __name__ == '__main__':
    s = SalvaVida()
    try:
        s.run()
    except KeyboardInterrupt:
        db_session.remove()
