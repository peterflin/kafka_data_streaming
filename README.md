# Streaming Data Using Python & Kafka

Using Python to retrieve data from a Kafka Queue and write it into MySQL.  
Additionally, using FastAPI to launch an API Server, through which a background task can be initiated by calling the API. This design allows further scheduling of tasks either through Airflow to set the timing or through other scheduling methods.


## Kafka
### Run Kafka Server
```
docker compose -f docker-compose.yml up -d
```

### Set Topic
We need to add new topic by hands using script in container
```bash
# get bash in kafka container
cd /opt/bitnami/kafka/bin

kafka-topics.sh \
--create \
--bootstrap-server localhost:9092 \
--replication-factor 1 \
--partitions 3 \
--topic future_price
```
parameter explanation:
- create: it means you want to create a topic
- bootstrap-server: your kafka servers
- replication-factor: how many replica you want to create when data push in topic
- partitions: how many partition in a topic you want to create
- topic: specify a topic name

## MySQL

### Run MySQL Server
```bash
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=msqylpwd mysql:8.0-bullseye
```

### Create Table
```SQL
-- build.sql
CREATE DATABASE IF NOT EXISTS `streaming_data`;
USE `streaming_data`;

CREATE TABLE IF NOT EXISTS `transaction_data` (
  `future_id` int(11) NOT NULL,
  `future_price` int(11) DEFAULT NULL,
  `procces_time` datetime NOT NULL,
  `create_time` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`future_id`,`procces_time`),
  KEY `INDEX` (`future_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## Python
### Version
3.8.10

### Package Install
```bash
pip install -r requirements.txt
```

### Run API server
```
cd streaming
uvicorn management:app --host 0.0.0.0 --port 8000
```

### Run Job
You can use `curl` or other way to send request to server
```
curl -X 'POST' 'http://localhost:8000/run' -H 'accept: application/json' -d ''
```

## Memo

### How to ensure that I won't get the same data when a topic have two or more consumer is consuming?
You can set a parameter which called `group_id` in Kafka.Consumer.
```python
consumer = kafka.KafkaConsumer(
    "future_price",
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf8')),
    group_id="stream"
)
```

## Next To Do
- Exception handling
- Testing on real data which from request
- Adjust config on Kafka
