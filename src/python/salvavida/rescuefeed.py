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

    def run(self):
        """ Setup TwitterStreamer. """

        app_key = self.config.get('twitter', 'app_key')
        app_secret = self.config.get('twitter', 'app_secret')
        oauth_token = self.config.get('twitter', 'oauth_token')
        oauth_token_secret = self.config.get('twitter', 'oauth_token_secret')
        self.stream = TwitterStreamer(app_key, app_secret, oauth_token,
            oauth_token_secret)
        self.stream.set_tags(self.feed_tags)
        self.stream.statuses.filter(track=self.feed_tags)

class TwitterStreamer(TwythonStreamer):
    """ Salva Vida main class."""

    def set_tags(self, feed_tags):
        self.feed_tags = feed_tags

    def on_success(self, data):
        if 'text' in data:
            try:
                if any(x.upper() in data['text'].upper()
                    for x in self.feed_tags):
                    (tag, name, address) = data['text'].split('/')
                elif reply_tags in data['text']:
                    pass
                (lat, long) = Geocoder.geocode(address)[0].coordinates
                f = Feed(name=name,lat=lat,long=long)
                db_session.add(f)
                db_session.commit()
                print Feed.query.all()
            #        print Feed.query.filter(User.name.uppercase == 'RICK')
            except DBAPIError as e:
                print e
            except DisconnectionError as e:
                db_session.remove()
                db_session.init()
            except Exception as e:
                print e
                logging.error(e)
                pass
    

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
