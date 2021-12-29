
import pika, json

channel = None

# queue = 'admin'
queue = 'main'

def connect():

    channel = None
    try:

        # https://cluster.provider-2.prod.ewr1.akash.pub:31082/
        # ---
        # https://cluster.provider-2.prod.ewr1.akash.pub
        # 31082

        url = 'amqp://guest:guest@cluster.provider-2.prod.ewr1.akash.pub:32408'
        # url = 'amqp://guest:guest@rabbit:5672'
        
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
    except pika.exceptions.AMQPConnectionError as e:
        print("ERR: Could not connect to rabbitmq\nErr description: {}".format(e))

    return channel


def publish(method, body):
    channel = connect()
    if channel is not None:
        properties = pika.BasicProperties(method)
        channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(body), properties=properties)
        print("published!")
        channel.close()
    else:
        print("ERR: Could not publish since no connection is established")