import base64
import json

import requests

with open('receipt_scanner/walmart.png', 'rb') as f:
    encodedImage = base64.b64encode(f.read())

payload = {'image': encodedImage}

r = requests.post('http://127.0.0.1:5000/uploadImage',
                  data=payload)
print(r)
