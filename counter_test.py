#!/usr/bin/python
# -*- coding: utf-8 *-*
#
#       Filename: index.py
#       Date:     2012-08-14
#       author:   Mathieu Charron <mathieu@hyberia.ca>
#       Project:  G-Anime Registration
#
#       Copyright 2012 Hyberia Inc.
#
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above copyright
#         notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the Hyberia Inc. nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#!/usr/bin/python

import web
from session import MongoStore
from pymongo import Connection

# Config
mongoDBConString = "mongodb://ganime:2EKY7BSN@127.0.0.1/registration"

web.config.debug = False
urls = (
    "/", "index",
    "/count", "count",
    "/reset", "reset",
    "/favicon.ico", "nothing"
)
web.config.session_parameters['cookie_name'] = 'reg_session_id'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['cookie_path'] = '/'
web.config.session_parameters['timeout'] = 86400, #24 * 60 * 60, # 24 hours   in seconds
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
web.config.session_parameters['secret_key'] = 'QGEHZAwBtsRQtEausprLqUtt'
web.config.session_parameters['expired_message'] = 'Session expired'

app = web.application(urls, locals())

# Initialize the MongoDB connection
connection = Connection(mongoDBConString)
db = connection.registration

#session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
#session = web.session.Session(app, MongoStore(db, 'sessions'), initializer={'count': 0})

class index:
    """Main index page"""
    def GET(self):
        web.setcookie("cart_id", "0", expires="300", path="/", domain=None, secure=False)

#        return str(session.count)
        return "Cookie Set"


class count:
    """Counting page"""
    def GET(self):
        """"""
        i = int(web.cookies().get("cart_id"))+1
        web.setcookie("cart_id", i, expires="300", path="/", domain=None, secure=False)
        return i
#        session.count += 1
#        return str(session.count)


class reset:
    """Count reset"""
    def GET(self):
        """"""
        web.setcookie("cart_id", "", expires="-1", path="/", domain=None, secure=False)
        return "Cookie Destroyed"


class nothing:
    """"""
    def GET(self):
        return ""

if __name__ == "__main__":
    app.run()
