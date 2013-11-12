import logging

import config

from daemon import runner
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

    def get_feed(self, name, lat, long):
        return Feed.query.filter(Feed.name==name, Feed.lat==lat,
                                 Feed.long==long).first()

    def on_success(self, data):
        if 'text' in data:
            try:
                (_, tag, name, address) = data['text'].split('/')
                result = Geocoder.geocode(address)
                (lat, long) = result[0].coordinates
                formatted_address = result[0].formatted_address
                feed = self.get_feed(name.upper(), lat, long)
                if feed:
                    # Filter dupes
                    logging.debug('Feed exists: %s' % (feed))
                    if tag.upper() in self.reply_tags.upper():
                        # The flask SQLAlchemy doesn't seem to have
                        # a method for updating. Weird.
                        db_session.delete(feed)
                        db_session.commit()
                        new_feed = Feed(name=name.upper(),lat=lat,long=long,
                               tag='safe',address=formatted_address)
                        db_session.add(new_feed)
                        db_session.commit()
                        logging.debug('Feed updated.')
                else:
                    f = Feed(name=name.upper(),lat=lat,long=long,
                             address=formatted_address)
                    db_session.add(f)
                    db_session.commit()
                    logging.debug('Feed created name=%s, lat=%s, long=%s.'\
                       'address=%s' % (name.upper(), lat, long, 
                       formatted_address))
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
#    sv_daemon = runner.DaemonRunner(s)
#    sv_daemon.do_action()
