#!/usr/bin/python
# -*- coding: utf-8 *-*
#
#       Filename: badge.py
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
import config
import datetime
import db
import tools
from view import render


class create:
    """Display and process a badge form"""
    def GET(self):
        cart_id = web.cookies().get(config.cookieName)
        if cart_id:
            f = config.formBadge()
            return render.base(render.badge(f), "Nouvel insigne ~ New badge", True)
        else:
             raise web.seeother(tools.make_url('/'))

    def POST(self):
        cart_id = web.cookies().get(config.cookieName)
        if cart_id:
            # We have a cart, proceed
            f = config.formBadge()
            if not f.validates():
                return render.base(render.badge(f), "Nouvel insigne ~ New badge", True)
            else:
                # Everything is valid, let's build the query
                badge = {
                    "prenom": f.d.prenom,
                    "nom": f.d.nom,
                    "texte_insigne": f.d.texte_insigne,
                    "courriel": f.d.courriel,
                    "adresse": {
                        "ligne_1": f.d.adresse_1,
                        "ligne_2": f.d.adresse_2,
                        "ville": f.d.ville,
                        "province": f.d.province,
                        "code_postal": f.d.code_postal
                        },
                    "type": f.d.type,
                    "telephone_urgence": f.d.telephone_urgence,
                    "extra": {
                        "noiz": f.d.noiz,
                        "tshirt": f.d.tshirt,
                        "dvd": f.d.dvd
                        },
                    "instructions_speciales": f.d.instructions_speciales,
                    "status": "IN_CART",
                    "date": datetime.datetime.utcnow()}

                # Adding to DB
                badge_id = db.addBadge(badge, cart_id)

                raise web.seeother(tools.make_url("/cart/add/%s" % badge_id))
        else:
             raise web.seeother(tools.make_url('/error'))

class edit:
    def GET(self, badge_id):
        cart_id = web.cookies().get(config.cookieName)
        if cart_id:
            f = config.formBadge()
            if not db.validObjectId(badge_id):
                raise web.seeother('/error')

            badge = db.getBadge(badge_id)
            badge["adresse_1"] = badge["adresse"]["ligne_1"]
            badge["adresse_2"] = badge["adresse"]["ligne_2"]
            badge["ville"] = badge["adresse"]["ville"]
            badge["province"] = badge["adresse"]["province"]
            badge["code_postal"] = badge["adresse"]["code_postal"]
            badge["noiz"] = badge["extra"]["noiz"]
            badge["tshirt"] = badge["extra"]["tshirt"]
            badge["dvd"] = badge["extra"]["dvd"]
            f.fill(badge)
            return render.base(render.badge(f), "Modifier une insigne ~ Edit a badge", True)
        else:
            raise web.seeother(tools.make_url('/error'))

    def POST(self, badge_id):
        cart_id = web.cookies().get(config.cookieName)
        if cart_id:
            # We have a cart, proceed
            f = config.formBadge()
            if not f.validates():
                return render.base(render.badge(f), "Editer une insigne ~ Edit a badge", True)
            else:
                # Everything is valid, let's build the query
                badge = {
                    "prenom": f.d.prenom,
                    "nom": f.d.nom,
                    "texte_insigne": f.d.texte_insigne,
                    "courriel": f.d.courriel,
                    "adresse": {
                        "ligne_1": f.d.adresse_1,
                        "ligne_2": f.d.adresse_2,
                        "ville": f.d.ville,
                        "province": f.d.province,
                        "code_postal": f.d.code_postal
                        },
                    "type": f.d.type,
                    "telephone_urgence": f.d.telephone_urgence,
                    "extra": {
                        "noiz": f.d.noiz,
                        "tshirt": f.d.tshirt,
                        "dvd": f.d.dvd
                        },
                    "instructions_speciales": f.d.instructions_speciales,
                    "status": "IN_CART"}

                # Adding to DB
                db.updateBadge(badge, badge_id)

                raise web.seeother(tools.make_url("/cart/update/%s" % badge_id))
        else:
             raise web.seeother(tools.make_url('/error'))

class display:
    def GET(self, badge_id):
        raise web.internalerror()

    def POST(self, badge_id):
        raise web.internalerror()
