from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
from enum import Enum

class Companies(Enum):
    google = "Google"
    facebook = "Facebook"
    twitter = "Twitter"
    github = "Github"
    amazon = "Amazon"
    
class VotingOptions(Enum):
    low = "low"
    middle = "middle"
    high = "high"
    
class Person:
    def __init__(self, id, isMem, AweCoin, stripeID,subscriptionId,VotedFor):
      self.id = id
      self.isMem = isMem
      self.AweCoin = AweCoin
      self.stripeID = stripeID
      self.subscriptionId = subscriptionId
      self.VotedFor = VotedFor
      
    def makeNewPerson(email,company):
     id = ObjectId()
    #  encryptedEmail = pbkdf2_sha256.hash(email)
     return {
            company : email,
            "_id" : str(id),
            "isMem" : False,
            "AweCoin" : 0,
            "stripeID" : "",
            "subscriptionID" : "",
            "VotedFor" : VotingOptions.middle.value
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

    