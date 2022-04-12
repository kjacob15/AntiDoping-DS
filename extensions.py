from pymongo import MongoClient
import certifi

ca = certifi.where()
DATABASE_URL=""
mongo_client = MongoClient('mongodb://ds-group7:oXnDNoD6PzBwQA9rAWZatjznb1ZU2O9Pg9SZzb1SzcgcrdcfEagt7UeaDCWJSYHVAxqbPN2Gwt5Oc0u4oy507Q==@ds-group7.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@ds-group7@',tlsCAFile=ca)
db = mongo_client['wada']