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
    low = -1
    middle = 0
    high = 1
    
class Person:
    def __init__(self, id, isMem, AweCoin, customerID,VotedFor):
      self.id = id
      self.isMem = isMem
      self.AweCoin = AweCoin
      self.customerID = customerID
      self.VotedFor = VotedFor
      
    def makeNewPerson(email,company):
     id = ObjectId()
    #  encryptedEmail = pbkdf2_sha256.hash(email)
     return {
            company : email,
            "_id" : str(id),
            "isMem" : False,
            "AweCoin" : 0,
            "customerID" : "",
            "VotedFor" : 0
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

    