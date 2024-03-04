import json
import kafka
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm_model import TransactionData


if __name__ == '__main__':
    sql_uri = os.getenv("sql_uri")
    if sql_uri is None:
        raise ValueError("Please set environment variable: sql_uri")
    engine = create_engine()
    session = sessionmaker(bind=engine)
    session = session()
    consumer = kafka.KafkaConsumer(
        "future_price",
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf8')),
        group_id="stream"
    )
    for msg in consumer:
        print(msg.partition, msg.offset, msg.value['process_time'])
        try:
            row_data = TransactionData(**msg.value)
            session.add(row_data)
            session.commit()
        except Exception as e:
            print(e)
