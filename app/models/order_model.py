from app.extensions import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(200), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    description =db.Column(db.String(255), nullable = False)
    status = db.Column(db.String(50), default='pending')  
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='orders')


    def __init__(self,item,quantity, description, status, total_price):
        super(Order, self).__init__()
        
        self.item = item
        self.quantity = quantity
        self.description = description
        self.status = status
        self.total_price =total_price
        
    def __repr__(self):
        return f'Order: {self.item} {self.status}'