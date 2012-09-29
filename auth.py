#!/usr/bin/python
# -*- coding: utf-8 *-*

import web
import logging
import config
import db
import hashlib
import view
from view import render
from urllib import urlencode
from urllib2 import urlopen, Request
import bson

logging.basicConfig(filename="/home/ganime/paypal-callback.log",level=logging.DEBUG)

def verify_ipn(data):
    # prepares provided data set to inform PayPal we wish to validate the response
    data["cmd"] = "_notify-validate"
    params = urlencode(data)

    # sends the data and request to the PayPal Sandbox
    req = Request("""%s/cgi-bin/webscr""" % (config.paypalUrl, ), params)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    # reads the response back from PayPal
    response = urlopen(req)
    status = response.read()

    # If not verified
    if not status == "VERIFIED":
        logging.debug("status is not verified")
        return False

    # if not the correct receiver ID
    #if not data.receiver_id == config.paypalId:
    #    logging.debug("receiver_id is %s" % (data.receiver_id, ))
    #    return False

    # if not the correct currency
    #if not data["mc_currency"] == "CAD":
    #    logging.debug("Wrong currency")
    #    return False

    # otherwise...
    return True

class notify:
    def GET(self):
        logging.debug("Callback GET")
        return ""
    def POST(self):
        data = web.input()
        logging.debug(data)
        # If there is no txn_id in the received arguments don't proceed
        if not "txn_id" in data:
            logging.debug("No txn_id")
            return "No Parameters"

        # Verify the data received with Paypal
        if not verify_ipn(data):
            logging.debug("Verification failed")
            return "CALLBACK_FAILED"
        logging.debug("IPN verification pass")

        # If verified, store desired information about the transaction
        transaction_data = {
            "txn": data["txn_id"],
            "amount": data["mc_gross"],
            "fee": data["mc_fee"],
            "email": data["payer_email"],
            "name": data["first_name"] + " " + data["last_name"],
            "status": data["payment_status"],
            "payment_date": data["payment_date"]
            }
        logging.debug("CART_ID %s" % (data["invoice"], ))
        logging.debug(transaction_data)
        # Update DB
        db.callbackBadge(data["invoice"], transaction_data)

        # Send email
        web.sendmail(config.email["debug_from"], config.email["debug"],
                     "IPN", transaction_data)
        hashEmail = hashlib.sha1()
        hashEmail.update(transaction_data["email"])
        hashEmail.update(config.salt)
        logging.debug("Sending confirmation email to %s" % (transaction_data["email"], ))
        web.sendmail(config.email["notice_from"], data["payer_email"],
                     "G-Anime Pre-Registration", render.e_val(data["invoice"], hashEmail.hexdigest(), transaction_data))
        return "CALLBACK_COMPLETE"

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
            raise web.seeother(config.make_url("/pickup/%s" % (cart_id, )))
        else:
           return  render.base("""<h2>Ce courriel est invalide</h2>""", "Confirmation", True)



class pickup:
    def GET(self, cart_id):
        """Display the badges associated with a Cart ID"""
        try:
            bson.objectid.ObjectId(cart_id)
        except bson.errors.InvalidId:
            return render.base(render.validate(None, ("bad", "Invalid ObjectId")), "Pickup", True)

        return render.base(render.pickup(view.badgeListing(cart_id)), "Pickup", True)