import logging
import os

import config

from datetime import datetime

from pygeocoder import Geocoder
from sqlalchemy.exc import DatabaseError, DBAPIError, SQLAlchemyError
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
        if os.getenv('HEROKU') is None:
            logging.basicConfig(filename=self.config.get('salvavida', 
                'logfile'), level=logging.DEBUG)
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
            except (SQLAlchemyError, DatabaseError) as e:
                logging.error(e)
            except ValueError as e:
                pass
            except (DBAPIError, Exception) as e:
                logging.error(e)
            finally:
                db_session.remove()
    

        # Want to disconnect after the first result?
        # self.disconnect()

    def on_error(self, status_code, data):
        logging.error('%s - %s' % (status_code, data))


if __name__ == '__main__':
    s = SalvaVida()
    s.run()
