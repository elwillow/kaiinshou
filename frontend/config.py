#!/usr/bin/python
# -*- coding: utf-8 *-*
#
#       Filename: config.py
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

# Sites configuration
from web import form

formBadge = form.Form(
    form.Textbox("prenom", form.notnull,
        description="Prénom / First Name"),
    form.Textbox("nom", form.notnull,
        description="Nom / Last Name"),
    form.Textbox("texte_insigne",
        description="Texte sur l'insigne / Texte on the badge"),
    form.Textbox("courriel", form.notnull,
        description="Courriel / Email"),

    form.Textbox("adresse_1", form.notnull,
        description="Adresse 1 / Address 1"),
    form.Textbox("adresse_2",
        description="Adresse 2 / Address 2"),
    form.Textbox("ville", form.notnull,
        description="Ville / City"),
    form.Dropdown("province",
        [
            ("", "Sélectionner"),
            ("AB", "Alberta (AB)"),
            ("BC", "British Columbia (BC)"),
            ("MB", "Manitoba (MB)"),
            ("NB", "New Brunswick (NB)"),
            ("NL", "Newfoundland and Labrador (NL)"),
            ("NT", "Northwest Territories (NT)"),
            ("NS", "Nova Scotia (NS)"),
            ("NU", "Nunavut (NU)"),
            ("PE", "Prince Edward Island (PE)"),
            ("SK", "Saskatchewan (SK)"),
            ("ON", "Ontario (ON)"),
            ("QC", "Québec (QC)"),
            ("YT", "Yukon (YT)"),
            ("USA", "USA"),
            ("OTHER", "Other / Autre"),
        ], form.notnull,
        description="Province / Province"),
    form.Textbox("code_postal", form.notnull,
        description="Code postal / Postal Code"),
    form.Textbox("telephone_urgence", form.notnull,
        description="Téléphone d'urgence / Emergency phone #"),
    # Type de badge
    form.Dropdown("type",
        [
            ("Weekend_Adulte", "Fin de semaine, Adulte / Weekend Pass, Adult ~ 35$"),
            ("Weekend_Jeune", "Fin de semaine, 8 à 12 ans / Weekend Pass, 8 to 12 years old ~ 20$"),
            ("Weekend_Enfant", "Fin de semaine, 0 à 7 ans / Weekend Pass, 0 to 7 years old ~ 0$"),
            ("Friday_Adulte", "Vendredi seulement, Adulte / Friday only, Adult ~ 25$"),
            ("Friday_Jeune", "Vendredi seulement, 8 à 12 ans / Friday only, 8 to 12 years old ~ 20$"),
        ], form.notnull,
        description="Type de billet / Ticket type"),
    form.Dropdown("noiz",
        [
            ("non", "Non / No"),
            ("oui", "Oui / Yes (20$)")
        ],
        value="non",
        description="Spectacle NOIZ (vendredi soir) / NOIZ show (Friday night)"),
    form.Dropdown("tshirt",
        [
            ("X", "Aucun / None"),
            ("P", "Petit / Small"),
            ("M", "Moyen / Medium"),
            ("G", "Grand / Large"),
            ("TG", "Très grand / X-large")
        ], description="T-Shirt", pre="20 $"),
    form.Dropdown("dvd",
        [
            ("non", "Non / No"),
            ("oui", "Oui / Yes (20$)")
        ],
        value="non",
        description="DVD de la mascarade / Masquerade DVD"),
    form.Textarea("instructions_speciales", rows=2, cols=40,
        description="Instructions spécial / Specials Instructions")
    )

codeBadge = {
    "A": ("Pré-inscription, Fin de semaine, Adulte", 35),
    "B": ("Pré-inscription, Fin de semaine, Jeune", 20),
    "C": ("Pré-inscription, Fin de semaine, Enfant", 0),
    "D": ("Inscription, Fin de semaine, Adulte", 45),
    "E": ("Inscription, Fin de semaine, Jeune", 25),
    "F": ("Inscription, Fin de semaine, Enfant", 0),
    "G": ("Inscription, Vendredi, Adulte", 45),
    "H": ("Inscription, Vendredi, Jeune", 25),
    "J": ("Inscription, Vendredi, Enfant", 0),
    "K": ("Inscription, Samedi, Adulte", 45),
    "L": ("Inscription, Samedi, Jeune", 25),
    "M": ("Inscription, Samedi, Enfant", 0),
    "N": ("Inscription, Dimanche, Adulte", 45),
    "P": ("Inscription, Dimanche, Jeune", 25),
    "Q": ("Inscription, Dimanche, Enfant", 0),

    "R": ("Artiste", -1),
    "S": ("Bénévole", -1),
    "T": ("Direction, Über-staff", -1),
    "U": ("Gratuit, Cadeau, Remerciement, VIP", -1),
    "V": ("Invité", -1),
    "W": ("Marchand", -1),
    "X": ("Média", -1),
    "Y": ("Sécurité", -1),
    "Z": ("Staff", -1)
}


# Web.py stuff
web.config.debug = True
#web.ctx.home = "https://secure.sajg.net/inscription"
web.ctx.home = "http://kaiinshou.hyberia.net/frontend/"
cache = False

# Initialize the MongoDB connection
connection = Connection(mongoURI)
DB = connection.registration