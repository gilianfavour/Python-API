from app.extensions import db

class Address(db.Model):
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='addresses')
    
    
    def __init__(self, city, country):
        super(Address,self).__init__()
        self.city = city
        self.country = country
        
        
    def __repr__(self):
        return f'Address: {self.city} {self.country}'