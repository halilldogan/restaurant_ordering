import redis
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()


# Initialize Redis connection
host = os.getenv("REDIS_HOST")
r = redis.StrictRedis(host=host, port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe('order_channel')

# Listen for messages
baseUrl = os.getenv("APP_BASEURL")
url = baseUrl + "/order/process_order/"

for message in pubsub.listen():
    if message['type'] == 'message':
        order_id = message['data']
        print(f'Received order ID: {order_id}')
        data = {
        "order_id": order_id  
        }
        time.sleep(3)
        response = requests.post(url=url, data=data)
        if response.status_code == 200:
            print(f'Order {order_id} processed successfully.')
        else:
            print(f'Failed to process order {order_id}. Error: {response.content}')