from .. import db

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False, index=True)
    holdings = db.relationship('Holding', backref='portfolio', cascade='all, delete-orphan', lazy=True)

class Holding(db.Model):
    __tablename__ = 'holdings'
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    coin_id = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Float, nullable=False)
