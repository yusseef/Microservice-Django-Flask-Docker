# amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb
import pika, json, os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product
params = pika.URLParameters('amqps://yildtheb:ZEATuey0rMa34bFIZ7NSmcUIQIhu4JFH@hawk.rmq.cloudamqp.com/yildtheb')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue = 'admin')

def callback(ch, method, properties, body):
    print('Message recieved')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    print('product likes increased')

channel.basic_consume(queue = 'admin', on_message_callback = callback, auto_ack= True)

print('started consuming....')

channel.start_consuming()

channel.close()