import kafka
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
from kafka_producer import produce_data


def run_job():
    server = kafka.KafkaProducer(bootstrap_servers=['kafka:9092'])
    scheduler = BlockingScheduler(jobstores={"mysql": SQLAlchemyJobStore("mysql+pymysql://root:mysql0119@172.24.32.1:3307/streaming_data")})
    scheduler.add_job(produce_data, 'date', next_run_time=datetime.now() + timedelta(seconds=10), args=(server, ), id='test')
    scheduler.start()
