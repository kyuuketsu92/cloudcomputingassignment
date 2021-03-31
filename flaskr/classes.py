from . import db, crypticarts
from flask_login import UserMixin

class User(UserMixin):
    name = "not loaded'blablabla'"
    def __init__(self, id, uname, passphrase, email, apiauthkey):
        self.id = id
        self.uname = uname
        self.passphrase = passphrase
        self.email = email
        self.api_autkey = apiauthkey

    def get_id(self):
        return self.id
    
    def get_name(self):
        self.name = crypticarts.decrypt(db.getName(self.id))
        return self.name #gotta check if the value is None

    def getkey(self):
        return crypticarts.decrypt(self.api_autkey)

