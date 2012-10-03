#!/usr/bin/python
# -*- coding: utf-8 *-*


import web
from pymongo import Connection

# Database configuration
#mongoURI = "mongodb://ganime:2EKY7BSN@127.0.0.1/registration-dev"
mongoURI = "mongodb://ganime:2EKY7BSN@127.0.0.1/registration"

# For testing puposes
#paypalAccount = "mathie_1345421600_biz@hyberia.ca"
#paypalUrl = "https://www.sandbox.paypal.com"
#paypalId = "9B3P56RWHB85Q"
paypalAccount = "finance@ganime.ca"
paypalUrl = "https://www.paypal.com"
paypalId = "SP2X3RHPES2HU"

cookieName = "ganime_cartid"
salt = "+828497786499849"
email = {
    "debug_from": "noreply@ganime.ca",
    "debug": "mathieu.charron@ganime.ca",
    "notice_from": "inscription@ganime.ca",
    }

# Web.py stuff
web.config.debug = True
#web.ctx.home = "https://secure.sajg.net/inscription"
web.ctx.home = "http://localhost/frontend/"
cache = False

# Initialize the MongoDB connection
connection = Connection(mongoURI)
DB = connection.registration

def make_url(url):
    """
    Fix an apparent incompatibility between how I'm using Apache URL rewriting
    and the web.seeother (and web.redirect, etc.) commands.

    - If input is full URL (i.e., http://example.com/blah/), return as is.
    - If input starts with "/", treat as relative to this application's base.
    - Otherwise, append it to the current URL, minus any ending filename.
    """
    import urlparse, os

    if "://" not in url:
        url_parts = list(urlparse.urlparse(web.ctx.env["REQUEST_URI"]))
        old_path = url_parts[2]

        if url.startswith("/"):
            #base = os.path.basename(__file__)
            base = "app.py"
            home = web.ctx.home
            if home.endswith(base) and not old_path.endswith(__file__):
                home = home[:0-len(base)]
            url = home.rstrip("/") + url
        else:
            new_path = os.path.normpath(os.path.join(old_path, url))
            url_parts[2] = new_path
            url = urlparse.urlunparse(url_parts)
    return url