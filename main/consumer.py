# amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb
import pika, json

from main import Product, db, app
from flask import current_app
params = pika.URLParameters('amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb')
app_ctx = app.app_context()
app_ctx.push()

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue = 'main')

def callback(ch, method, properties, body):
    print('Message recieved')

    data = json.loads(body)
    print(data)

    if properties.content_type == 'product created':
        print('product created')
        product = Product(id = data['id'], title = data['name'], image = data['image'])
        db.session.add(product)
        db.session.commit()

    elif properties.content_type == 'product updated':
        print('product updated')
        product = Product.session.get(data['id'])
        product.title = data['name']
        product.image = data['image']
        db.session.commit()

    elif properties.content_type == 'product deleted':
        print('product deleted')
        product = Product.session.get(data)
        db.session.delete(product)
        db.session.commit()


channel.basic_consume(queue = 'main', on_message_callback = callback, auto_ack= True)

print('started consuming....')

channel.start_consuming()

channel.close()