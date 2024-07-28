from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import User, Restaurant, Category, Dish, Order
from .serializers import UserSerializer, RestaurantSerializer, CategorySerializer, DishSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
import redis
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from dotenv import load_dotenv
import os
load_dotenv()

host = os.getenv("REDIS_HOST")
# Initialize Redis connection
r = redis.StrictRedis(host=host, port=6379, db=0)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    @action(detail=False, methods=['post'])
    def submit_order(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            # Publish order to Redis Pub/Sub
            r.publish('order_channel', order.id)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def list_orders(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class ProcessOrderView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'error': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=order_id)
            order.status = "Completed"
            order.save()
            return Response({'status': 'Order processed'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)