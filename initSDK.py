import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./privkey.json")
firebase_admin.initialize_app(credential = cred, options = {
    'projectId' : 'portable-fridge-c194f'
})

db = firestore.client()

doc_ref = db.collection(u'user')
docs = doc_ref.stream()

for doc in docs:
    print(doc.id, doc.to_dict())

