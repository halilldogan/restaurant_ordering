from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Restaurant, Category, Dish, Order
from rest_framework.test import APIRequestFactory


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        self.admin_user = User.objects.create_user(username='adminuser', password='adminpass', email='admin@example.com')
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', address='123 Test St', admin=self.admin_user)
        self.category = Category.objects.create(name='Test Category')
        self.dish = Dish.objects.create(name='Test Dish', price=9.99, category=self.category)
        self.dish.restaurant.add(self.restaurant)
        self.order_data = {
            'user': self.user.id,
            'dishes': [self.dish.id],
            'status': 'pending',
            'restaurant': self.restaurant.id
        }

    def test_submit_order(self):
        url = reverse('order-submit-order')
        response = self.client.post(url, self.order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().status, 'pending')

    def test_process_order(self):
        order = Order.objects.create(user=self.user, status='pending', restaurant=self.restaurant)
        order.dishes.add(self.dish)
        url = reverse('process_order')
        response = self.client.post(url, {"order_id": order.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, 'Completed')

    def test_list_orders(self):
        order1 = Order.objects.create(user=self.user, status='pending', restaurant=self.restaurant)
        order1.dishes.add(self.dish)
        order2 = Order.objects.create(user=self.user, status='completed', restaurant=self.restaurant)
        order2.dishes.add(self.dish)
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    
