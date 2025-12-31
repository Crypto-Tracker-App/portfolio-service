from ..models.portfolio import Portfolio, Holding
from .. import db

class PortfolioService:
    @staticmethod
    def get_portfolio(user_id):
        return Portfolio.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_total_net_holding(user_id):
        portfolio = PortfolioService.get_portfolio(user_id)
        if not portfolio:
            return 0.0
        return sum(h.amount for h in portfolio.holdings)

    @staticmethod
    def add_holding(user_id, coin_id, amount):
        portfolio = Portfolio.query.filter_by(user_id=user_id).first()
        if not portfolio:
            portfolio = Portfolio(user_id=user_id)
            db.session.add(portfolio)
            db.session.commit()
        holding = Holding.query.filter_by(portfolio_id=portfolio.id, coin_id=coin_id).first()
        if holding:
            holding.amount += amount
        else:
            holding = Holding(portfolio_id=portfolio.id, coin_id=coin_id, amount=amount)
            db.session.add(holding)
        db.session.commit()
        return holding

    @staticmethod
    def remove_holding(user_id, coin_id):
        portfolio = Portfolio.query.filter_by(user_id=user_id).first()
        if not portfolio:
            return False
        holding = Holding.query.filter_by(portfolio_id=portfolio.id, coin_id=coin_id).first()
        if not holding:
            return False
        db.session.delete(holding)
        db.session.commit()
        return True
