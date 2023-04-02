from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
from enum import Enum

class Companies(Enum):
    google = 'Google'
    facebook = "Facebook"
    twitter = "Twitter"
    github = "Github"
    Amazon = "Amazon"
    
    

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

def makeNewPerson(email,company):
     id = ObjectId()
     encryptedEmail = pbkdf2_sha256.hash(email)
     return {
            company : encryptedEmail,
            "_id" : str(id),
            "isSubscribed" : False,
            "AweCoin" : 0,
            "paymentEmail" : ""
        }
     
def returningPersonCheck(email,company,DB):
     encryptedEmail = pbkdf2_sha256.hash(email)
     if pbkdf2_sha256.verify(email,encryptedEmail):
        person_found = DB.find_one({company: encryptedEmail})
     return person_found
    