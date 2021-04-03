from . import db, crypticarts
from flask_login import UserMixin

class User(UserMixin):
    name = None
    def __init__(self, id, uname, passphrase, email, apiauthkey):
        self.id = id
        self.uname = uname
        self.passphrase = passphrase
        self.email = email
        self.api_autkey = apiauthkey

    def get_id(self):
        return self.id
    
    def get_name(self):
        name = db.getName(self.id)
        if name is None:
            self.name = None;
        else:
            self.name = crypticarts.decrypt(name)
        return self.name #gotta check if the value is None

    def getkey(self):
        return crypticarts.decrypt(self.api_autkey)

    def got_name_set(self):
        self.get_name()
        if self.name is None:
            return False
        else:
            return True

