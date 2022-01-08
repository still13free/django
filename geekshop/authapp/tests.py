from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.conf import settings


class AuthUserTestCase(TestCase):
    status_ok = 200
    status_redirect = 302
    username = 'django'
    password = 'geekbrains'

    def setUp(self) -> None:
        self.client = Client()
        self.superuser = ShopUser.objects.create_superuser(
            username=self.username,
            password=self.password,
        )

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

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'пользователь',
                               status_code=self.status_ok)

        self.client.login(username=self.username, password=self.password,)

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.status_code, self.status_ok)

        response = self.client.get('/')
        self.assertContains(response, 'пользователь',
                            status_code=self.status_ok)

    def test_redirect(self):
        # product = Product.objects.first()
        # response = self.client.get(f'/basket/add/{product.pk}')
        # self.assertEqual(response.status_code, self.status_redirect)

        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, self.status_redirect)

        self.client.login(username=self.username, password=self.password,)
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('Ваша корзина, пользователь', response.content.decode())

    def test_user_logout(self):
        self.client.login(username=self.username, password=self.password,)

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, self.status_redirect)

        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertTrue(response.context['user'].is_anonymous)

        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'sumuel@geekshop.local',
            'age': '21',
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, self.status_redirect)

        new_user = ShopUser.objects.get(username=new_user_data['username'])

        activation_url = f"{settings.BASE_URL}/auth/verify/{new_user_data['email']}/{new_user.activate_key}/"

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_ok)

        self.client.login(
            username=new_user_data['username'], password=new_user_data['password1'])

        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.status_ok)
        self.assertFalse(response.context['user'].is_anonymous)

        response = self.client.get('/')
        self.assertContains(
            response, text=new_user_data['first_name'], status_code=self.status_ok)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Мэри',
            'last_name': 'Поппинс',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'merypoppins@geekshop.local',
            'age': '17',
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, self.status_ok)
        self.assertFormError(response, 'register_form',
                             'age', 'Too young to die!')
