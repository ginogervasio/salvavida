SalvaVida
===========

**A Python + Flask + Twython + Twitter + Google Maps + Twilio (Soon) Rescue Dispatch App**

This is a rescue dispatch app for calamities like Typhoon Yolanda.  It reads twitter streams for sos calls and plots them on a map.  Similar in functionality to [rescueph.com](http://rescueph.com) but filters for dupes and saves.

This is intended for the National Disaster Risk Reduction Council who want to know which areas need the most urgent attention.  The map displays clusters of markers.  Larger clusters mean more people need help in that area.

How it works
-------------

If a person is in trouble, tweet '@SalvaVidaPH\sos\Name\Address' and a marker will be set on the map.

e.g. @SalvaVidaPH\sos\Sterling Archer\2401 Taft Ave, 1004 Manila

If a person is rescued, tweet '@SalvaVidaPH\Safe\Name\Address' and the marker will be removed.

e.g. @SalvaVidaPH\safe\Sterling Archer\2401 Taft Ave, 1004 Manila

Run the app on your local machine
----------------------------------

* Go to dev.twitter.com and make an app to get the app keys, app secrets, oauth token and oauth token secrets

* Add salvavida.cfg to your etc/ with the following contents:

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

* Start the twitter streamer with:
` python src/python/salvavida/rescuefeed.py `

* Start the flask app with:
` python app.py `

Future plans
-------------
- Add SMS functionality
- Add FB news feed reader/graph search stream reader

License
-------

The MIT License (MIT)

Copyright (c) 2013 Gino Gervasio http://salvavida.org

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.