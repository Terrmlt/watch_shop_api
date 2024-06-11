from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from products.models import Product, Brand
from products.serializers import ProductSerializer, CreateOrUpdateProductSerializer

UserModel = get_user_model()


class ProductAPITest(APITestCase):
    url = '/api/v1/products/'

    def setUp(self):
        self.brand = Brand.objects.create(name='Test Brand')
        self.products = [
            Product.objects.create(name='Test Product 1',
                                   brand=self.brand,
                                   description='Test Product Description 1',
                                   price=10.25,
                                   quantity=2),
            Product.objects.create(name='Test Product 2',
                                   brand=self.brand,
                                   description='Test Product Description 2',
                                   price=32.05,
                                   quantity=4),
            Product.objects.create(name='Test Product 3',
                                   brand=self.brand,
                                   description='Test Product Description 3',
                                   price=75.00,
                                   quantity=5),
        ]
        user_client = UserModel.objects.create(username='client', password='client_password_123')
        access = str(RefreshToken.for_user(user_client).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

        user_manager = UserModel.objects.create(username='manager', password='manager_password_123', is_manager=True)
        access = str(RefreshToken.for_user(user_manager).access_token)
        self.manager = APIClient(HTTP_AUTHORIZATION='Bearer ' + access)

        self.anonymous = APIClient()

    def test_product_list(self):
        anonymous_response = self.anonymous.get(self.url)
        self.assertEqual(anonymous_response.status_code, status.HTTP_200_OK)

        response_data = anonymous_response.data['results']
        self.assertEqual(len(response_data), Product.objects.count())

        expected_product_data = ProductSerializer(instance=self.products, many=True).data
        self.assertListEqual(response_data, expected_product_data)

    def test_product_detail(self):
        product = self.products[0]

        response = self.anonymous.get(f'{self.url}{product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        expected_product_data = ProductSerializer(instance=product).data

        self.assertDictEqual(expected_product_data, response_data)

    def test_product_create(self):
        new_product_data = {
            'name': 'New Product',
            'brand': self.brand.id,
            'description': 'New Product Description',
            'price': 22.00,
            'quantity': 4
        }

        anonymous_response = self.anonymous.post(self.url, new_product_data)
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        client_response = self.client.post(self.url, new_product_data)
        self.assertEqual(client_response.status_code, status.HTTP_403_FORBIDDEN)

        manager_response = self.manager.post(self.url, new_product_data)
        self.assertEqual(manager_response.status_code, status.HTTP_201_CREATED)

        comparing_data = manager_response.data
        expected_data = CreateOrUpdateProductSerializer(
            {'id': comparing_data['id'], **new_product_data, 'brand': self.brand}).data

        self.assertDictEqual(comparing_data, expected_data)

    def test_product_partial_update(self):
        product = self.products[0]
        new_data = {'name': 'New Name'}
        product.name = new_data['name']

        anonymous_response = self.anonymous.patch(f'{self.url}{product.id}/', new_data)
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        client_response = self.client.patch(f'{self.url}{product.id}/', new_data)
        self.assertEqual(client_response.status_code, status.HTTP_403_FORBIDDEN)

        manager_response = self.manager.patch(f'{self.url}{product.id}/', new_data)
        self.assertEqual(manager_response.status_code, status.HTTP_200_OK)

        comparing_data = ProductSerializer(instance=Product.objects.get(id=product.id)).data
        expected_data = ProductSerializer(instance=product).data

        self.assertDictEqual(comparing_data, expected_data)

    def test_product_update(self):
        product = self.products[0]
        other_brand = Brand.objects.create(name='Other Brand')
        new_data = {'brand': other_brand.id,
                    'name': 'New Name',
                    'description': 'New Description',
                    'price': 77.44,
                    'quantity': 1}

        anonymous_response = self.anonymous.put(f'{self.url}{product.id}/', new_data)
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        client_response = self.client.put(f'{self.url}{product.id}/', new_data)
        self.assertEqual(client_response.status_code, status.HTTP_403_FORBIDDEN)

        manager_response = self.manager.put(f'{self.url}{product.id}/', new_data)
        self.assertEqual(manager_response.status_code, status.HTTP_200_OK)

        comparing_data = ProductSerializer(instance=Product.objects.get(id=product.id)).data
        expected_data = ProductSerializer({**new_data, 'brand': other_brand, 'id': product.id}).data

        self.assertDictEqual(comparing_data, expected_data)

    def test_product_delete(self):
        product = self.products[0]

        anonymous_response = self.anonymous.delete(f'{self.url}{product.id}/')
        self.assertEqual(anonymous_response.status_code, status.HTTP_401_UNAUTHORIZED)

        client_response = self.client.delete(f'{self.url}{product.id}/')
        self.assertEqual(client_response.status_code, status.HTTP_403_FORBIDDEN)

        manager_response = self.manager.delete(f'{self.url}{product.id}/')
        self.assertEqual(manager_response.status_code, status.HTTP_204_NO_CONTENT)
