# coding: utf-8
from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TransactionData(Base):
    __tablename__ = 'transaction_data'

    future_id = Column(INTEGER(11), primary_key=True, nullable=False, index=True)
    future_price = Column(INTEGER(11))
    process_time = Column(DateTime, primary_key=True, nullable=False)
    create_time = Column(DateTime, server_default=text("current_timestamp()"))
