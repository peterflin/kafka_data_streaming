import kafka
import json
from datetime import datetime
import time
import random


def produce_data(server):
    for i in range(1, 51):
        row = {"future_id": i, "future_price": random.randint(10, 1000), "process_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        future = server.send('future_price', json.dumps(row, ensure_ascii=False).encode("utf8"))
        result = future.get(timeout=10)
        print(result)
    server.close()


if __name__ == "__main__":
    produce_data()
