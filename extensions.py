import os
from pymongo import MongoClient
import certifi

ca = certifi.where()
uri= os.environ.get("DATABASE_URL")
mongo_client = MongoClient(uri,tlsCAFile=ca)
db = mongo_client['wada']