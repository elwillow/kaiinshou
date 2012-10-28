#!/usr/bin/python
# -*- coding: utf-8 *-*
#
#       Filename: auth.py
#       Date:     2012-08-14
#       author:   Mathieu Charron <mathieu@hyberia.ca>
#       Project:  Kaiinshou
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

import web
import logging
import config
import db
import tools
import hashlib
from view import render
import bson

logging.basicConfig(filename="/home/elwillow/paypal-callback.log",level=logging.DEBUG)

class email:
    """Validate an email and display the badges associated with it"""
    def GET(self, cart_id, hash):
        """Validate an email and forward to the pickup page"""
        try:
            bson.objectid.ObjectId(cart_id)
        except bson.errors.InvalidId:
            return render.base(render.validate(None, ("bad", "Invalid ObjectId")), "Confirmation", True)

        cart = db.getCart(cart_id)
        if not cart:
            return render.base("""<h2>Ce courriel est invalide</h2>""", "Confirmation", True)

        vEmail = hashlib.sha1()
        vEmail.update(cart["email"])
        vEmail.update(config.salt)
        if vEmail.hexdigest() == hash:
            db.cartValidEmail(cart_id)
            raise web.seeother(tools.make_url("/receipt/%s" % (cart_id, )))
        else:
           return  render.base("""<h2>Ce courriel est invalide</h2>""", "Confirmation", True)
