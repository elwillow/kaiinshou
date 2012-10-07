#!/usr/bin/python
# -*- coding: utf-8 *-*

import web
from web import form
import config
import datetime
import db
from view import render

badgeForm = form.Form(
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


class create:
    """Display and process a badge form"""
    def GET(self):
        cart_id = web.cookies().get(config.cookieName)
        if cart_id:
            f = badgeForm()
            return render.base(render.badge(f), "Nouvel insigne ~ New badge", True)
        else:
             raise web.seeother(config.make_url('/error'))

    def POST(self):
        cart_id = web.cookies().get(config.cookieName)
        if cart_id:
            # We have a cart, proceed
            f = badgeForm()
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

                raise web.seeother(config.make_url("/cart/add/%s" % badge_id))
        else:
             raise web.seeother(config.make_url('/error'))

class edit:
    def GET(self, badge_id):
        cart_id = web.cookies().get(config.cookieName)
        if cart_id:
            f = badgeForm()
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
            raise web.seeother(config.make_url('/error'))

    def POST(self, badge_id):
        cart_id = web.cookies().get(config.cookieName)
        if cart_id:
            # We have a cart, proceed
            f = badgeForm()
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

                raise web.seeother(config.make_url("/cart/update/%s" % badge_id))
        else:
             raise web.seeother(config.make_url('/error'))

class display:
    def GET(self, badge_id):
        raise web.internalerror()

    def POST(self, badge_id):
        raise web.internalerror()
