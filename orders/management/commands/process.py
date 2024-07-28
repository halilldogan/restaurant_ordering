from django.core.management.base import BaseCommand
import redis
from orders.models import Order

class Command(BaseCommand):
    help = 'Process orders from Redis Pub/Sub'

    def handle(self, *args, **kwargs):
        r = redis.StrictRedis(host='redis', port=6379, db=0)
        pubsub = r.pubsub()
        pubsub.subscribe('order_channel')
        
        for message in pubsub.listen():
            if message['type'] == 'message':
                order_id = int(message['data'])
                order = Order.objects.get(id=order_id)
                # Process the order (e.g., mark as completed)
                order.status = Order.COMPLETED
                order.save()
                self.stdout.write(self.style.SUCCESS(f'Order {order_id} processed'))
