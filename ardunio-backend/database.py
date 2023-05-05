from pymongo import MongoClient
import certifi

ca = certifi.where()

client=MongoClient("mongodb+srv://Neo:neoasdfgh@cluster0.gysxidy.mongodb.net/?retryWrites=true&w=majority",
                   tlsCAFile=ca)

db=client["Arduino"]
user_col = db["user"]
heat_col=db["heat"]

