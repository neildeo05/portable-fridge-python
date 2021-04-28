# Guide
## Authentication Header:
POST request with username, password:
returns back JWT token

## Route explanation
  - /createProfile
    - POST
      - request data(json): 'user id', 'username', 'email', 'preferences', 'username'
      - response: 200 or 404
  - /getProfile
    - GET
      - request data(params): 'id'
      - response: json data of user
