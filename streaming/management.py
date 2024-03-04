from fastapi import FastAPI
from schedule import run_job
from apscheduler.schedulers.background import BackgroundScheduler
import kafka
from kafka_producer import produce_data
from datetime import datetime, timedelta


app = FastAPI()


@app.post("/run")
def run():
    server = kafka.KafkaProducer(bootstrap_servers=['kafka:9092'])
    scheduler = BackgroundScheduler()
    scheduler.add_job(produce_data, 'date', next_run_time=datetime.now() + timedelta(seconds=10), args=(server, ), id='test')
    scheduler.start()
    return "done"
