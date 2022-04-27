from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_name = Column(String)
    balance = Column(Integer)

    def execute_balance(self):
        return self.balance

    def __repr__(self):
        return "<Player(%r, %r)>" % (
            self.player_name, self.balance
        )
