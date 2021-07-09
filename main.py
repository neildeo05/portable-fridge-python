import base64
import io
# import cv2
# import matplotlib.pyplot as plt
# import numpy as np
from firebase_admin import credentials, firestore, initialize_app
from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from flask_cors import CORS
CRED = credentials.Certificate("privkey.json")
initialize_app(credential=CRED, options={
           'projectId': 'portablefridge-311105'})
db = firestore.client()
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "7479f7fc-66cb-4a01-950a-b30b5807f8bf"
CORS(app)
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
# @app.route('/uploadImage', methods=['POST'])
# @jwt_required()
# def uploadImage():
    # current_user = get_jwt_identity()
    # image has to be b64encoded before sending request
    # byteImage = base64.b64decode(request.form.to_dict()['image'])
    # image = Image.open(io.BytesIO(byteImage))
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    # Image.fromarray(image).save('buff.jpg')
    # ocr.main()

    # return jsonify({'status': True})
# Inventory API
@app.route('/updateItems', methods=['POST', 'PUT'])
@jwt_required()
def addItems():
    current_user = get_jwt_identity()
    try:
        uid = request.json['uid']
        if uid:
            [t.update(request.json) for t in db.collection(
                'user').document(uid).collection('inventory').stream()]
            return jsonify({'status': True}), 200
        else:
            print('Please follow schema for inventory items')
            return jsonify({'status': False}), 404
    except Exception as e:
        print(e)


@app.route('/getInventory', methods=['GET'])
@jwt_required()
def getInventory():
    current_user = get_jwt_identity()
    try:
        uid = request.args.get('id')
        return jsonify(
            [doc.to_dict() for doc in db.collection('users').document(
                uid).collection('inventory').stream()]
        )
    except Exception as e:
        print(e)


# recipes
@app.route('/getCommunityRecipes', methods=['GET'])
@jwt_required()
def getCommunityRecipes():
    current_user = get_jwt_identity()
    try:
        uid = request.args.get('id')
        if uid:
            user_ref = db.collection('users')
            user_doc = user_ref.document(uid)
            prefs = user_doc.get().to_dict()['preferences']
            # inv = [i.to_dict()
            #        for i in user_doc.collection('inventory').stream()]
            # curr_inv = inv[0]
            all_recipes = [i.to_dict()
                           for i in db.collection('recipe').stream()]
            return (jsonify({"recipes": all_recipes}), 200)
    except Exception as e:
        print(e)


@app.route('/postRecipes', methods=['POST'])
@jwt_required()
def createRecipe():
    current_user = get_jwt_identity()
    try:
        rid = request.json['id']
        if rid:
            db.collection('recipe').document(rid).set(request.json)
            return jsonify({"status": True}), 200
        else:
            return ("RID not present in request query", 404)
    except Exception as e:
        print(e)


@app.route('/getRecipes', methods=['GET'])
@jwt_required()
def getRecipe():
    current_user = get_jwt_identity()
    try:
        rid = request.args.get('id')
        if rid:
            recipe = db.collection('recipe').document(rid).get()
            return (jsonify(recipe.to_dict()), 200)
        else:
            return jsonify([doc.to_dict() for doc in db.collection('recipe').stream()])
    except Exception as e:
        print(e)


@app.route('/likeRecipe', methods=['POST'])
@jwt_required()
def likeRecipe():
    current_user = get_jwt_identity()
    try:
        rid = request.json['id']
        if rid:
            prev_likes = db.collection('recipe').document(
                rid).get().to_dict()['likes']
            print(prev_likes)
            db.collection('recipe').document(
                rid).update({"likes": prev_likes+1})
            return "True"
            # db.collection('recipe').document(rid).update({'likes': })
        print(request.json)
        return "FALSE"
    except Exception as e:
        print(e)


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=8080)
