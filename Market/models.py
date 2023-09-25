from Market import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer, nullable=False, default=15000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    
    def __repr__(self):
        return f'Item {self.username}'
    
    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]} $'
        else:
            return f'{self.budget} $'
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def password_check(self, password_attempt):
        return bcrypt.check_password_hash(self.password_hash, password_attempt)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    description = db.Column(db.String(length=1024), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'Item {self.name}'
    
    @property
    def prettier_price(self):
        if len(str(self.price)) >= 4:
            return f'{str(self.price)[:-3]},{str(self.price)[-3:]} $'
        else:
            return f'{self.price} $'
