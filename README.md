SalvaVida
===========

A Python + Flask + Twython + Twitter + Google Maps + Twilio (Soon) Rescue Dispatch App
-------------------------------------------------------------------------------

This is a rescue dispatch app for calamities like Typhoon Yolanda.  It reads twitter streams for sos calls and plots them on a map.  Similar in functionality to [rescueph.com](http://rescueph.com) but filters for dupes and saves.

This is intended for the National Disaster Risk Reduction Council who want to know which areas need the most urgent attention.  The map displays clusters of markers.  Larger clusters mean more people need help in that area.

How to use:
-----------

If a person is in trouble, tweet '@SalvaVidaPH\sos\Name\Address' and a marker will be set on the map.

e.g. @SalvaVidaPH\sos\Sterling Archer\2401 Taft Ave, 1004 Manila

If a person is rescued, tweet '@SalvaVidaPH\Safe\Name\Address' and the marker will be removed.

e.g. @SalvaVidaPH\safe\Sterling Archer\2401 Taft Ave, 1004 Manila

Run the app on your local machine
----------------------------------

1. Go to dev.twitter.com and make an app to get the app keys, app secrets, oauth token and oauth token secrets

2. Add salvavida.cfg to your etc/ with the following contents:

```
 [twitter]
app_key=<CONSUMER KEY>
app_secret=<CONSUMER SECRET>
oauth_token=<ACCESS TOKEN>
oauth_token_secret=<ACCESS TOKEN SECRET>
feed_tags=<KEYWORDS TO FILTER>

[salvavida]
logfile=<LOGFILE>

[db]
uri=sqlite:////tmp/sv.db

```
3. Start the twitter streamer with:
` python src/python/salvavida/rescuefeed.py `

4. Start the flask app with:
` python app.py `

Future plans
-------------
- Add SMS functionality
- Add FB news feed reader/graph search stream reader