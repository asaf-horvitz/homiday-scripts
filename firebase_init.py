import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

def connect_to_db():
    cred = credentials.Certificate('service_account.json')

    firebase_admin.initialize_app(cred)
    # firebase_admin.initialize_app(cred, {
    #     'storageBucket': 'home-263917.appspot.com'
    # })
    return firestore.client()

db = connect_to_db()

def get_db():
    
    return db