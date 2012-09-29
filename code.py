#!/usr/bin/python
# -*- coding: utf-8 *-*
#
#       Filename: code.py
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


import web, os, urlparse
import view
import config
import db
from view import render

urls = (
    "/", "index",
    "/cart/(.*)/(.*)", "cartManagement",
    "/validate/(.*)/email/(.*)", "auth.email",
    "/pickup/(.*)", "auth.pickup",
    "/badge", "badge.create",
    "/badge/(.*)", "badge.display",
    "/edit/(.*)", "badge.edit",
    "/callback", "auth.notify",
    "/merci", "thanks"
)


class index:
    """Main index page"""
    def GET(self):
        """Display the cart listing"""
        cart_id = web.cookies().get(config.cookieName)
        if not cart_id:
            cart_number = view.generateCartNumber()
            cart_id = db.newCart(cart_number)
            view.saveCookie(cart_id)
        return render.base(view.cartListing(cart_id))


class cartManagement:
    def GET(self, action, badge_id):
        cart_id = view.getCookie()
        if not cart_id:
            raise web.seeother(config.make_url("/"))

        return render.base(view.cartListing(cart_id, (action, badge_id)))


class thanks:
    """Thanks the shopper and delete the cookie"""
    def GET(self):
        """"""
        view.destroyCookie()
        return render.base("""<p>Votre session est maintenant terminé. Vérifier vos courriels pour votre confirmation d'inscription.</p>
        <p>Pour toutes questions, contactez <a href="mailto:inscription@ganime.ca">inscription@ganime.ca</a>""")


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
