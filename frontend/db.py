#!/usr/bin/python
# -*- coding: utf-8 *-*

import config
#import view
import datetime
import bson
from bson import objectid

def validObjectId(o):
    try:
        if bson.objectid.ObjectId(o):
            return True
    except bson.errors.InvalidId:
        return False

def newCart(cartNumber):
    """Add a new cart to the collections"""
    cart = {"cart_number": cartNumber,
        "date": datetime.datetime.utcnow()}

    return config.DB.carts.insert(cart)

def getCart(cart_id):
    """Return the array for a given cart"""
    return config.DB.carts.find_one({"_id": objectid.ObjectId(cart_id)})

def cartValidEmail(cart_id):
    config.DB.carts.find_and_modify({"_id": objectid.ObjectId(cart_id)}, {"$set": {"valid_email": True}})
    return True

def addBadge(badge, cart_id=None):
    """
    Add a new badge to the database and update the cart if necessary
    and return the badge ID
    """
    if cart_id:
        # This is an online purchase
        if config.DB.carts.find_one({"_id": objectid.ObjectId(cart_id)}):
            # Get the badge number
            badge_number = config.DB.counters.find_and_modify({"_id": "badges"}, {"$inc": {"num": 1}})
            badge["badge_number"] = int(badge_number["num"])
            badge_id = config.DB.badges.save(badge)
            if badge_id:
                # Update the cart with the badge ObjectId
                config.DB.carts.update({"_id": objectid.ObjectId(cart_id)}, {"$addToSet": {"badges": badge_id}})
                return badge_id
            else:
                return None
        return None
    else:
        # No valid card
        return None

def updateBadge(badge, badge_id):
    """
    Update a Badge in the database and return the badge ID
    """
    config.DB.badges.find_and_modify({"_id": objectid.ObjectId(badge_id)}, {"$set": badge})
    return True

def callbackBadge(cart_id, data):
    # Check if a cart exists
    if not config.DB.carts.find_one({"_id": objectid.ObjectId(cart_id)}):
        return False

    # update the cart with new information
    if config.DB.carts.update({"_id": objectid.ObjectId(cart_id)}, {"$set": data}):
        return True

    # @TODO Update the badges so they show as valid

    # something went wrong
    else:
        return False

def getBadgeList(cart_id):
    """Return all the badges in a given cart"""
    try:
        badges = config.DB.carts.find_one({"_id": objectid.ObjectId(cart_id)})["badges"]
    except KeyError:
        badges = None
    except TypeError:
        badges = None
    return badges

def getBadgesDetail(badges):
    """Return an array matching every ObjectID passed"""
    return list(config.DB.badges.find({"_id": {"$in": badges}}))

def getBadge(badge_id):
    """Return a single badge detail"""
    return config.DB.badges.find_one({"_id": objectid.ObjectId(badge_id)})

