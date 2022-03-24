from django.test import TestCase
from django.urls import reverse

from apps.account.utils import generate_token
from apps.account.models import Account

class AccountTests(TestCase):
    
    def __init__(self, methodName: str = ...) -> None:
        self.payload ={
            'email': 'test@example.com',
            'password': 'TestpassUltra1',
            'username': 'userTest',
        }
        super().__init__(methodName)


    def test_register_user(self):
        register_payload={
            'email': 'test@example.com',
            'password1': 'TestpassUltra1',
            'password2': 'TestpassUltra1',
            'username': 'userTest',
        }
        response = self.client.post(reverse('register'), data={**register_payload})
        self.assertEqual(response.status_code, 302)


    def test_register_user_fail(self):
        register_payload={
            'email': 'test@example.com',
            'password1': 'TestpassUltra1',
            'password2': 'TestpassUltra1',
            'username': 'userTest',
        }
        user = Account.objects.create_user(**self.payload)
        user.is_active=True
        user.save()
        response = self.client.post(reverse('register'), data={**register_payload})
        self.assertEqual(response.status_code, 400)


    def test_user_login(self):
        login_payload={
            'username': 'userTest',
            'password': 'TestpassUltra1'
        }
        user = Account.objects.create_user(**self.payload)
        user.is_active=True
        user.save()
        response = self.client.post(reverse('login'), data={**login_payload})
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_login(self):
        login_payload={
            'password': 'TestpassUltra1',
            'username': 'userTest',
        }
        user=Account.objects.create_user(**self.payload)
        user.is_active=False
        user.save()
        response = self.client.post(reverse('login'), data={**login_payload})
        self.assertEqual(response.status_code, 400)