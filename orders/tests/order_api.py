from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from products.models import Product, Brand

UserModel = get_user_model()


class OrderAPITest(APITestCase):
    url = '/api/v1/orders/'

    def setUp(self):
        self.user_client = UserModel.objects.create(username='client', password='client_password_123')
        access = str(RefreshToken.for_user(self.user_client).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

        user_manager = UserModel.objects.create(username='manager', password='manager_password_123', is_manager=True)
        access = str(RefreshToken.for_user(user_manager).access_token)
        self.manager = APIClient(HTTP_AUTHORIZATION='Bearer ' + access)

        self.anonymous = APIClient()

        self.brand = Brand.objects.create(name='Test Brand')
        self.products = [
            Product.objects.create(name='Test Product 1',
                                   brand=self.brand,
                                   description='Test Product Description 1',
                                   price=10.25,
                                   quantity=10),
            Product.objects.create(name='Test Product 2',
                                   brand=self.brand,
                                   description='Test Product Description 2',
                                   price=32.05,
                                   quantity=10),
            Product.objects.create(name='Test Product 3',
                                   brand=self.brand,
                                   description='Test Product Description 3',
                                   price=75.00,
                                   quantity=10),
        ]

        self.order = Order.objects.create(user=self.user_client, address='Test Address')
        self.order_items = [
            OrderItem.objects.create(order=self.order, product=self.products[0], quantity=1),
            OrderItem.objects.create(order=self.order, product=self.products[0], quantity=3),
            OrderItem.objects.create(order=self.order, product=self.products[0], quantity=7),
        ]

        self.other_user_client = UserModel.objects.create(username='other_user_client',
                                                          password='password1234',
                                                          is_manager=False)

        self.other_client_order = Order.objects.create(user=self.other_user_client, address='Test Address')
        self.other_client_order_items = [
            OrderItem.objects.create(order=self.other_client_order, product=self.products[0], quantity=3),
            OrderItem.objects.create(order=self.other_client_order, product=self.products[1], quantity=3),
            OrderItem.objects.create(order=self.other_client_order, product=self.products[2], quantity=3),
        ]

        access = str(RefreshToken.for_user(self.other_user_client).access_token)
        self.other_client = APIClient(HTTP_AUTHORIZATION='Bearer ' + access)

    def test_order_list(self):
        anonymous_response = self.anonymous.get(self.url)
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        client_response = self.client.get(self.url)
        self.assertEqual(client_response.status_code, status.HTTP_403_FORBIDDEN)

        manager_response = self.manager.get(self.url)
        self.assertEqual(manager_response.status_code, status.HTTP_200_OK)

        comparing_data = manager_response.data['results']
        expected_data = OrderSerializer([self.order, self.other_client_order], many=True).data
        self.assertEqual(comparing_data, expected_data)

    def test_client_order_list(self):
        # запрет анонимному пользователю
        anonymous_response = self.anonymous.get(f'{self.url}my/?client_id={self.user_client.id}')
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        # доступно клиенту со свомими данными
        client_response = self.client.get(f'{self.url}my/?client_id={self.user_client.id}')
        self.assertEqual(client_response.status_code, status.HTTP_200_OK)

        # запрет клиенту смотреть чужие данные
        other_client_response = self.other_client.get(f'{self.url}my/?client_id={self.user_client.id}')
        self.assertEqual(other_client_response.status_code, status.HTTP_403_FORBIDDEN)

        # доступно клиенту со свомими данными
        other_client_response = self.other_client.get(f'{self.url}my/?client_id={self.other_user_client.id}')
        self.assertEqual(other_client_response.status_code, status.HTTP_200_OK)

        # доступно менеджеру смотреть данные клиента
        manager_response = self.manager.get(f'{self.url}my/?client_id={self.user_client.id}')
        self.assertEqual(manager_response.status_code, status.HTTP_200_OK)

        self.assertNotEquals(other_client_response.data, client_response.data)

    def test_order_detail(self):
        order = self.order

        anonymous_response = self.anonymous.get(f'{self.url}{order.id}/')
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        client_response = self.client.get(f'{self.url}{order.id}/')
        self.assertEqual(client_response.status_code, status.HTTP_200_OK)

        other_client_response = self.other_client.get(f'{self.url}{order.id}/')
        self.assertEqual(other_client_response.status_code, status.HTTP_403_FORBIDDEN)

        manager_response = self.manager.get(f'{self.url}{order.id}/')
        self.assertEqual(manager_response.status_code, status.HTTP_200_OK)

        comparing_data = client_response.data
        expected_data = OrderSerializer(order).data

        self.assertEqual(comparing_data, expected_data)

    def test_product_create(self):
        new_product_data = {
            'address': 'test adress',
            'items': [
                {'product': self.products[0].id, 'quantity': 10},
                {'product': self.products[1].id, 'quantity': 1},
            ]
        }

        anonymous_response = self.anonymous.post(self.url, new_product_data, format='json')
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        client_response = self.client.post(self.url, data=new_product_data, format='json')
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)

        order_id = client_response.data['id']
        existed_order = Order.objects.get(id=order_id)

        self.assertIsNotNone(existed_order)
