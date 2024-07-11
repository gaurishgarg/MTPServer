from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv()
uri = "mongodb+srv://this_user:passwordKey@projectvalues.z63yi4r.mongodb.net/?retryWrites=true&w=majority&appName=ProjectValues"
uri = uri.replace("this_user",os.getenv('MONGOUSER'))
uri = uri.replace("passwordKey",os.getenv('MONGOPASSWORD'))
client = MongoClient(uri, server_api=ServerApi('1'))
MTP_Database = client["MTP"]
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def returnclient():
    return client
def returndatabase():
    return MTP_Database