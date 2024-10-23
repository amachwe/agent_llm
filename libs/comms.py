import logs as logs
import typing as t
import pika as pk
import threading as th

HOST = "localhost"
K_TAG = "tag"

def dispatch_rabbitmq_topic(host: str, topic_name: str,text: str, tag: str  ) -> bool:
    try:
        with pk.BlockingConnection(pk.ConnectionParameters(host)) as connection:
            channel = connection.channel()
            if channel.exchange_declare(exchange=topic_name, exchange_type='fanout'):
                properties = pk.BasicProperties(
                    headers={K_TAG: tag}  # include the tag in the headers
                )
                channel.basic_publish(exchange=topic_name, routing_key='', body=text, properties=properties)
                logs.log_info(f"Sent {topic_name}", f"{text}, {K_TAG}={tag}")

                return True
    except Exception as e:
        logs.log_error(e)
        return False   


def dispatch_rabbitmq_queue(host: str, queue_name: str, text: str, tag: str) -> bool:
    
    with pk.BlockingConnection(pk.ConnectionParameters(host)) as connection:
        channel = connection.channel()
        if channel.queue_declare(queue=queue_name, durable=True):
            properties = pk.BasicProperties(
                headers={K_TAG: tag}  # include the tag in the headers
            )
            
            channel.basic_publish(exchange='', routing_key=queue_name, body=text, properties=properties)
            logs.log_info(f"Sent {queue_name}", f"{text}, {K_TAG}={tag}")
            connection.close()
            return True
    return False

def dispatch_message(host:str, dest_name:str, text: str, tag: str, dispatch_fn: t.Callable[[str,str,str], bool]=dispatch_rabbitmq_queue)->bool:
    if dispatch_fn:
        logs.log_info(f"Dispatching {text} to {dest_name}")
        return dispatch_fn(host, dest_name, text, tag)
    


def consumer_rabbitmq_queue(host: str,queue_name: str, callback: t.Callable[[str, str, pk.BasicProperties, str], None] = None)-> t.Optional[th.Thread]:

    def consumer_threaded():
        with pk.BlockingConnection(pk.ConnectionParameters(host)) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
    try:
        consumer_thread = th.Thread(target=consumer_threaded, daemon=True)
        consumer_thread.start()
        logs.log_info("Queue Consumer started", tag=queue_name)
    except Exception as e:
        logs.log_error(e)
        return None
    return consumer_thread


def consumer_rabbitmq_topic(host:str, topic_name:str, callback: t.Callable[[str, str, pk.BasicProperties, str], None] = None)-> t.Optional[th.Thread]:

    def consumer_threaded():
        with pk.BlockingConnection(pk.ConnectionParameters(host)) as connection:
            channel = connection.channel()
            channel.exchange_declare(exchange=topic_name, exchange_type='fanout')
            result = channel.queue_declare(queue='', exclusive=True)
            temp_queue_name = result.method.queue
            channel.queue_bind(exchange=topic_name, queue=temp_queue_name)
            channel.basic_consume(queue=temp_queue_name, on_message_callback=callback, auto_ack=True)
            channel.start_consuming()
    try:
        consumer_thread = th.Thread(target=consumer_threaded, daemon=True)
        consumer_thread.start()
        logs.log_info("Topic Consumer started", tag=topic_name)
    except Exception as e:
        logs.log_error(e)
        return consumer_thread
    return None
    


if __name__=="__main__":
    
    Q_Name = "test"
    Topic_Name = "topic_test"
    HOST = "localhost"

    def callback_q(ch, method, properties, body):
        print(f"Queue Received {body} {properties.headers[K_TAG]}")

    def callback_t(ch, method, properties, body):
        print(f"Topic Received {body} {properties.headers[K_TAG]}")

    t1 = consumer_rabbitmq_queue( host=HOST, queue_name=Q_Name, callback=callback_q)
    t2= consumer_rabbitmq_topic(host=HOST, topic_name=Topic_Name, callback=callback_t)
            
    def test_dispatch_q():
        for i in range(0,100):
            print(f"Q   Test{i}")
            dispatch_message(HOST, Q_Name, f"Test{i}", "test", dispatch_fn=dispatch_rabbitmq_queue)

    def main_q():
        thread_sender = th.Thread(target=test_dispatch_q)
        thread_sender.start()

    def test_dispatch_t():
        for i in range(0,100):
            print(f"T   Test{i}")
            dispatch_message(HOST, Topic_Name, f"Test{i}", "test", dispatch_fn=dispatch_rabbitmq_topic)

    def main_t():
        thread_sender = th.Thread(target=test_dispatch_t)
        thread_sender.start()



    main_q()

    main_t()
        

# class Event(dict):

#     def __init__(self, event_name:str, event_data:dict) -> None:
#         self.event_name = event_name
#         for k,v in event_data.items():
#             self[k] = v
    
#     def get_event_name(self):
#         return self.event_name

# class EventDispatcher(object):

#     def __init__(self):
#         self._consumers = []
    
#     def add_consumer(self, consumer: t.Callable[[str,Event], None]):
#         self._consumers.append(consumer)

#     def dispatch(e:Event):
#         def _dispatch(self, e:Event):
#             for c in self._consumers:
#                 try:
#                     c(e.get_event_name(), e)
#                 except Exception as e:
#                     pass

#         thread = th.Thread(target=_dispatch, args=(e.get_event_name(),e))
#         thread.start()
        