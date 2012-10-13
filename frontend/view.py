#!/usr/bin/python
# -*- coding: utf-8 *-*
#
#       Filename: view.py
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
import random
import db
import config


def badgeInfo(item):
    itemName = ""
    tps = 0
    tvq = 0
    if item["type"] == "Weekend_Adulte":
        itemName = itemName + "Adulte"
        cost = 35
        tps = tps + 1.52
        tvq = tvq + 3.04
    if item["type"] == "Friday_Adulte":
        itemName = itemName + "Adulte (Ven.)"
        cost = 25
        tps = tps + 0,87
        tvw = tvq + 1,73
    elif item["type"] == "Weekend_Jeune":
        itemName = itemName + "Jeune"
        cost = 20
    elif item["type"] == "Friday_Jeune":
        itemName = itemName + "Jeune (Ven.)"
        cost = 15
    elif item["type"] == "Weekend_Enfant":
        itemName = itemName + "Enfant"
        cost = 0

    # Extras
    if item["extra"]["noiz"] == "oui":
        itemName = itemName + " + NOIZ"
        cost = cost + 20
    if item["extra"]["tshirt"] != "X":
        itemName = itemName + " + T-Shirt (%s)" % (item["extra"]["tshirt"], )
        cost = cost + 20
    if item["extra"]["dvd"]:
        itemName = itemName + " + DVD"
        cost = cost + 20

    return itemName, cost, (tps, tvq)

def builtPaypalInput(item, i):
    itemName = "Badge %d: %s" % (item["badge_number"], badgeInfo(item)[0])

    return """<input type="hidden" name="item_name_%(i)d" value="%(name)s" /> <input type="hidden" name="amount_%(i)d" value="%(value).2f" />""" \
        % {"i": i, "name": itemName, "value": badgeInfo(item)[1]}


t_globals = dict(
  datestr=web.datestr,
  builtPaypalInput=builtPaypalInput,
  badgeInfo=badgeInfo,
  homeAddr=web.ctx.home,
  paypalUrl=config.paypalUrl,
  paypalAccount=config.paypalAccount,
)


render = web.template.render('templates/', cache=config.cache,
    globals=t_globals)
render._keywords['globals']['render'] = render


def generateCartNumber():
    """Generate a 8 characters cart number for easy identification"""
    word = ""
    for i in range(8):
        word += random.choice("0123456789abcdef")
    return word

def saveCookie(data):
    """Save a cookie containing `data`"""
    return web.setcookie("ganime_cartid", data, expires="3600", path="/",
        domain=None, secure=False)

def getCookie():
    """Return the information from cookie"""
    return web.cookies().get(config.cookieName)

def destroyCookie():
    """Destroy the cookie"""
    return web.setcookie(config.cookieName, "", expires="-1", path="/",
        domain=None, secure=False)

def cartListing(cart_id, messageInfo=None):
    """Return the HTML rendered list of items in the cart"""
    badges = db.badgeList(cart_id)
    if not badges:
        badgesDetail = None
    else:
        badgesDetail = db.badgesDetail(badges)
    return render.cart(cart_id, badgesDetail, messageInfo)

def badgeList(cart_id):
    """Return a array of badges from a cart id"""
    return db.badgesDetail(db.badgeList(cart_id))

def badgeListing(cart_id):
    """Return a HTML rendered list of badge from a cart id"""
    badges = db.badgeList(cart_id)
    if not badges:
        badgesDetail = None
    else:
        badgesDetail = db.badgesDetail(badges)
    return render.list(badgesDetail)