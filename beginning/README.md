# Beginner Service

When a new flight message is received, it checks the type and updates the message accordingly .
A simple flight send to the main processing queue .
ALL flight updates object in Radis,Checking the flight type for each sub-flight, updating the flight-message and sending it to the central processing queue .

## installation

Clone the repository.

 ```bash

git clone https://github.com/Green2Moon/SkylineAutomation.git
```

Build the image service

 ```bash
docker build -t <name> .
```

Run redis container:

```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

Run rabbitmq container:

```bash
docker run -it --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management
```

This will run a RabbitMQ container exposing the AMQP port (5672) and the management HTTP port (15672)

to start run this service you need to run from terminal in python container:

## Usage

```bash
 python main.py
 
 ```
