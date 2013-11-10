import logging
import config

from twython import TwythonStreamer

class SalvaVida():
    """ Main class. """

    def __init__(self):
        """ Constructor."""

        self.db = dict() # Use DB later
        c = config.Config()
        self.config = c.cfg
        logging.basicConfig(filename=self.config.get('salvavida', 'logfile'),
            level=logging.DEBUG)

    def run(self):
        """ Setup TwitterStreamer. """

        app_key = self.config.get('twitter', 'app_key')
        app_secret = self.config.get('twitter', 'app_secret')
        oauth_token = self.config.get('twitter', 'oauth_token')
        oauth_token_secret = self.config.get('twitter', 'oauth_token_secret')
        self.stream = TwitterStreamer(app_key, app_secret, oauth_token,
            oauth_token_secret)
        self.stream.statuses.filter(track=self.config.get('twitter', 'tags'))

class TwitterStreamer(TwythonStreamer):
    """ Salva Vida main class."""

    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')
        # Want to disconnect after the first result?
        # self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data


if __name__ == '__main__':
    s = SalvaVida()
    s.run()        
