import base64
import io

import cv2
import matplotlib.pyplot as plt
import numpy as np
from firebase_admin import credentials, firestore, initialize_app
from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from PIL import Image

import spec
from receipt_scanner.src import ocr

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "7479f7fc-66cb-4a01-950a-b30b5807f8bf"
jwt = JWTManager(app)


@app.route('/getToken', methods=["POST"])
def auth():
    username = request.json['username']
    passw = request.json['password']
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/createProfile", methods=['POST'])
@jwt_required()
def createProfile():
    current_user = get_jwt_identity()
    try:
        uid = request.json['id']
        if uid:
            db.collection('users').document(uid).set(request.json)
            return jsonify({"status": True}), 200
        else:
            return ("Tried to access user id that is not present in the database", 404)
    except Exception as e:
        print(e)


@app.route('/getProfile', methods=['GET'])
@jwt_required()
def getProfile():
    current_user = get_jwt_identity()
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
@jwt_required()
def updateProfile():
    current_user = get_jwt_identity()
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
@jwt_required()
def deleteProfile():
    current_user = get_jwt_identity()
    try:
        uid = request.args.get('id')
        db.collection("users").document(uid).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

# Scanner API
@app.route('/uploadImage', methods=['POST'])
def uploadImage():
    byteImage = base64.b64decode(request.form.to_dict()['image'])
    image = Image.open(io.BytesIO(byteImage))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    Image.fromarray(image).save('buff.jpg')
    ocr.main()
    return jsonify({'status': True})
# Inventory API
@app.route('/updateItems', methods=['POST', 'PUT'])
def addItems():
    try:
        iid = request.json['id']
        if iid:
            db.collection('inventory').document(iid).update(request.json)
            return jsonify({'status': True}), 200
        else:
            print('Please follow schema for inventory items')
            return jsonify({'status': False}), 404
    except Exception as e:
        print(e)

@app.route('/getInventory', methods=['GET'])
def getInventory():
    try:
        iid = request.args.get('id')
        if iid:
            user = db.collection('inventory').document(iid).get()
            return (jsonify(user.to_dict()), 200)
        else:
            return jsonify([doc.to_dict() for doc in db.collection('inventory').stream()])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    CRED = credentials.Certificate("privkey.json")
    initialize_app(credential=CRED, options={
                   'projectId': 'portable-fridge-c194f'})
    db = firestore.client()
    app.run()
