from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
from enum import Enum

class Companies(Enum):
    google = 'Google'
    facebook = "Facebook"
    twitter = "Twitter"
    github = "Github"
    Amazon = "Amazon"
    
class VotingOptions(Enum):
    low = -1
    middle = 0
    high = 1
    
class Person:
    id = ""
    isSubscribed = False
    AweCoin = 0
    paymentID = ""
    
    def __init__(self, id, isSubscribed, AweCoin, paymentID):
      self.id = id
      self.isSubscribed = isSubscribed
      self.AweCoin = AweCoin
      self.paymentID = paymentID
      
    def makeNewPerson(email,company):
     id = ObjectId()
     encryptedEmail = pbkdf2_sha256.hash(email)
     return {
            company : encryptedEmail,
            "_id" : str(id),
            "isSubscribed" : False,
            "AweCoin" : 0,
            "paymentID" : ""
        }

NewsPost = {
    'DateandTime' : "",
    'MessageText' : "",
    'MessageImage' : "",
    'ImageLink' : ""
}

Products = {
    'ProductImage' : "",
    'ProductAweCoin' : "",
    'ProductDescription' : ""
}


    # def returningPersonCheck(email,company,DB):
    #  encryptedEmail = pbkdf2_sha256.hash(email)
    #  isReturning = False
    #  if pbkdf2_sha256.verify(email,encryptedEmail):
    #     person_found = DB.find_one({company: encryptedEmail})
    #     isReturning = True
    #  return isReturning

    