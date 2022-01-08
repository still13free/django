from django.test import TestCase
from django.test.client import Client
from mainapp.models import ProductCategory, Product
from django.core.management import call_command

# class TestMainappPaginatorTestCase


class TestMainappSmoke(TestCase):
    status_ok = 200
    status_redirect = 302

    def setUp(self) -> None:
        # call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')

        self.category = ProductCategory.objects.create(
            name='category_1'
        )

        for i in range(5):
            Product.objects.create(
                name=f'product_{i}',
                category=self.category,
                short_desc='shortdesc',
                description='desc',
            )

        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.status_ok)

    def test_products_urls(self):
        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, self.status_ok)

    def test_categories_urls(self):
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, self.status_ok)

    # def tearDown(self):
    #     call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
