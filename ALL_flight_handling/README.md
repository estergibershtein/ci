# End-edit service

When a simple flight is received, it is sent to Skyline
A sub-flight will update the object in redis If all the subflights have completed the process so far, the parent flight (ALL) will be sent to Skyline .

## installation

redis container:

```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

rabbitmq container:

```bash
docker run -it --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```

This will run a RabbitMQ container exposing the AMQP port (5672) and the management HTTP port (15672)

to start run this service you need to run from terminal in python container:

## Usage

```bash
 pip install .
 python main.py
 ```
