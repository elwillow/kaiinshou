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

import view
from view import render
import bson

class pickup:
    def GET(self, cart_id):
        """Display the badges associated with a Cart ID"""
        try:
            bson.objectid.ObjectId(cart_id)
        except bson.errors.InvalidId:
            return cart_id
            #return render.base(render.receipt(), "Pickup", True)
        # calculate the taxes
        numbers = {"tps": 0, "tvq": 0, "taxes": 0, "sub": 0, "total": 0}
        badgesList = view.badgeList(cart_id)
        badges = []

        for b in badgesList:
            badge = view.badgeInfo(b)
            numbers["tps"] = numbers["tps"] + badge[2]["tps"]
            numbers["tvq"] = numbers["tvq"] + badge[2]["tvq"]
            numbers["total"] = numbers["total"] + badge[1]
            badges.append(badge)

        # get the sub-total and total
        numbers["taxes"] = numbers["tps"] + numbers["tvq"]
        numbers["sub"] = numbers["total"] - numbers["taxes"]

        return render.base(render.receipt(badgesList, badges, numbers), "Receipt", True)