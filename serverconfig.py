import pymongo
import os
import hashlib
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb+srv://ruben:JbFfpMejl9vtWQrG@database.35ntz.mongodb.net/database?retryWrites=true&w=majority")

secret = "5537f6d70a473013bfa284bbaca4f525"
state = hashlib.sha256(os.urandom(1024)).hexdigest()