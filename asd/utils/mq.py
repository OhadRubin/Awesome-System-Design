import pika

def connect2exchange(addr='localhost', exchange_name='packet'):
    # print("hi")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=addr))
    # , heartbeat = 600,
    # blocked_connection_timeout = 300
    channel = connection.channel()
    result = channel.queue_declare(queue='', exclusive=True)
    channel.exchange_declare(exchange=exchange_name,
                             exchange_type='fanout')
    channel.queue_bind(exchange=exchange_name,
                       queue=result.method.queue)
    return channel, result.method.queue


