from firebase_admin import credentials, firestore, initialize_app
from flask import Flask, jsonify, request

app = Flask(__name__)
CRED = credentials.Certificate("privkey.json")
initialize_app(credential=CRED, options={'projectId': 'portable-fridge-c194f'})
db = firestore.client()


@app.route("/createProfile", methods=['POST'])
def createProfile():
    try:
        uid = request.json['id']
        print(uid)
        if uid:
            db.collection('users').document(uid).set(request.json)
            return jsonify({"status": True}), 200
        else:
            return ("Tried to access user id that is not present in the database", 404)
    except Exception as e:
        print(e)


@app.route('/getProfile', methods=['GET'])
def getProfile():
    try:
        uid = request.args.get('id')
        print(uid)
        if uid:
            user = db.collection('users').document(uid).get()
            return (jsonify(user.to_dict()), 200)
        else:
            return jsonify([doc.to_dict() for doc in db.collection('users').stream()])
    except Exception as e:
        print(e)


@app.route('/updateProfile', methods=['POST', 'PUT'])
def updateProfile():
    try:
        uid = request.json['id']
        print(uid)
        if uid:
            db.collection('users').document(uid).update(request.json)
            return jsonify({"status": True}), 200
        else:
            return ("Tried to access user id that is not present in the database", 404)
    except Exception as e:
        print(e)


@app.route('/deleteProfile', methods=['GET', 'DELETE'])
def deleteProfile():
    try:
        uid = request.args.get('id')
        db.collection("users").document(uid).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


if __name__ == "__main__":
    print(db.collection('users').document(
        'mA5mfS5KW6Dk5tkMEoqb').get().to_dict())
    app.run()
