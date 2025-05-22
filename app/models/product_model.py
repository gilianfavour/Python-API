from flask import Flask
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',  backref='products')
    
    
    def __init__(self, name, price, stock, description):
        super(Product,self).__init__()
        self.name = name
        self.price = price
        self.stock = stock
        self.description
        
    def __repr__(self):
        return f'Product: {self.name} {self.description}'