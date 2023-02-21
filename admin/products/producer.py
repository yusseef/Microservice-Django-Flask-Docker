# amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb
import pika

params = pika.URLParameters('amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish():
    channel.basic_publish(exchange = '', routing_key = 'main', body = 'hello')
