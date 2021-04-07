class Spec:
    def toDict(self):
        pass
class InventorySpec(Spec):
    def __init__(self, items, userKey):
        self.items = items
        self.userKey = userKey
    def toDict(self):
        return {'items': self.items, 'userKey': self.userKey}

class RecipeSpec(Spec):
    def __init__(self, ingredients, name):
        self.ingredients = ingredients
        self.name = name
    def toDict(self):
        return {'ingredients': self.ingredients, 'name': self.name}

class UsersSpec(Spec):
    def __init__(self, email, password, preferences, username):
        self.email = email
        self.password = password
        self.preferences = preferences
        self.username = username
    def toDict(self):
        return {'email': self.email, 'password': self.password, 'preferences': self.preferences, 'username': self.username}
    

# tests

if __name__ == '__main__':
    i_s = InventorySpec(['cabbage', 'lettuce', 'leaves', 'taco seasoning'], 'Wu69Zss4Bd1hkokAMNUS')
    r_s = RecipeSpec(['cabbage', 'lettuce', 'leaves', 'taco seasoning'], 'zopf')
    u_s = UsersSpec('neilhdeo@gmail.com', 'foo', ['meat'], 'neild')
    print(i_s.toDict())
    print(r_s.toDict())
    print(u_s.toDict())
