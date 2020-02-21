import pika

def connect2exchange(addr='localhost', exchange_name='packet'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(addr))
    channel = connection.channel()
    result = channel.queue_declare(queue='', exclusive=True)
    channel.exchange_declare(exchange=exchange_name,
                             exchange_type='fanout')
    channel.queue_bind(exchange=exchange_name,
                       queue=result.method.queue)
    return channel, result.method.queue


