# amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb
import pika, json



params = pika.URLParameters('amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange = '',
     routing_key = 'admin',
      body = json.dumps(body),
       properties=properties)
