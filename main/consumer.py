# amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb
import pika

params = pika.URLParameters('amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue = 'main')

def callback(ch, method, properties, body):
    print('Message recieved')
    print(body)
    
channel.basic_consume(queue = 'main', on_message_callback = callback, auto_ack= True)

print('started consuming....')

channel.start_consuming()

channel.close()