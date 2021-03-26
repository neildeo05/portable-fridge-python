# Python Firestore Manual

We are going to create Firestore triggers, which handle POST/GET requests. As of now, there is no indication on whether we will host these functions on GCP, heroku, AWS, or Azure.

NOTICE: If you attended the last meeting, you can skip steps 1/2 (downloading and dreating a private key)
## Guide
 1. Download necessary dependencies.
    - In order to interact with the firestore database, we have to utilize the firebase admin sdk
    ```console
    $ pip install firebase-admin
    ```
    - We will need Flask to create an API that other subteams can make requests to
        ```console
        $ pip install flask
        ```
2. Generating Credentials 
    - If you haven't done so already, please contact Neil/Arihan to get added to the Firebase project and get access to the firebase console
    - After that, click on the gear icon, and navigate to Project settings/Service accounts
    - On the bottom, you should see a button to generate a new private key to interact with the Admin SDK
    - Click on generate private key, and wait for the install to finish
    - Move the resulting json file to your project directory
    - Change the name to private-key.json
3. Creating a python script
    - This will be done in the meeting. If you miss the meeting, please contact Neil or Arihan to get the details




USECASES
-----------

User X has a receipt. He scans the receipt, and some of the items are missing. He inputs in the missing items, and the items are 
stored in an inventory, along with his userID, and a timestamp. He wants a recipe, and using the items from the inventory, we recommend for him to make soup. We remove the items from his inventory


DATA MODEL (for now)
----------
```
User Collection
  L Information document
    L userid
    L username
    L email
    L password (hash-encoded)
  L Preferences Document
    L [ignoredIngredients]

Inventory
  L userInventory
    L userid
    L [items]
    L timeCreated

```
