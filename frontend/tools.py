#!/usr/bin/python
# -*- coding: utf-8 *-*
#
#       Filename: tools.py
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

import config
import web

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