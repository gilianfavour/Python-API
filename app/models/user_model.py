from flask import Flask
from app.extensions import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    userType = db.Column(db.Boolean, default=False)
    
    
    def __init__(self, userName, email, password, userType):
        super(User,self).__init__()
        self.userName = userName
        self.email = email
        self.password = password
        self.userType = userType
        
        
    def __repr__(self):
        return f'User: {self.userName} {self.userType}'