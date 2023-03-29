from accounts.models import User

from django.core.signing import Signer
from django.test import Client
from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.data = {
            'username': 'user_1',
            'password1': '123qwe!@#',
            'password2': '123qwe!@#',
            'email': 'user_1@test.com'
        }
        self.client = Client()  # эмуляция действий браузера
        self.registration_url = reverse('accounts:register')
        self.registration_done_url = reverse('accounts:register_done')

    def test_registration_valid(self):
        response = self.client.post(self.registration_url, self.data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)
        self.assertEqual(response.url, self.registration_done_url)

        user = User.objects.first()
        self.assertEqual(user.username, self.data['username'])
        self.assertEqual(user.email, self.data['email'])
        self.assertTrue(user.check_password(self.data['password1']))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_activated)

    def test_registration_invalid(self):
        self.data['password2'] = '123qwe!@'

        response = self.client.post(self.registration_url, self.data)
        self.assertNotEqual(response.status_code, 302)
        self.assertFalse(response.context['form'].is_valid())
        user = User.objects.filter(username=self.data['username'])
        self.assertEqual(len(user), 0)

    def test_activation_url(self):
        response = self.client.post(self.registration_url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)

        user = User.objects.first()

        self.assertEqual(user.username, self.data['username'])

        signer = Signer()
        # эмулируем клик по созданной ссылке
        response = self.client.get(
            'http://localhost' + reverse('accounts:register_activate', kwargs={'sign': signer.sign(user.username)})
        )
        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()  # имеющегося пользователя обновляем данными из базы
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_activated)

    def test_login_valid(self):
        response = self.client.post(self.registration_url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)

        user = User.objects.first()
        self.assertEqual(user.username, self.data['username'])

        login_url = reverse('accounts:login')
        login_data = {
            'username': 'user_1',
            'password': '123qwe!@#',
        }

        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(user.username, login_data['username'])
        self.assertTrue(user.check_password(login_data['password']))

    def test_login_invalid(self):
        response = self.client.post(self.registration_url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)

        user = User.objects.first()
        self.assertEqual(user.username, self.data['username'])

        login_url = reverse('accounts:login')
        login_data = {
            'username': 'user_2',
            'password': '123qwe!@',
        }

        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, 200)

        self.assertNotEqual(user.username, login_data['username'])
        self.assertFalse(user.check_password(login_data['password']))

    def test_user_repeat_send_url(self):
        response = self.client.post(self.registration_url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.registration_done_url, status_code=302, target_status_code=200)

        user = User.objects.first()
        self.assertEqual(user.username, self.data['username'])

        user_repeat_send_url = reverse('accounts:resend')
        user_repeat_send_done_url = reverse('accounts:email_done')
        user_repeat_send_data = {
            'email': 'user_1@test.com',
        }
        response = self.client.post(user_repeat_send_url, user_repeat_send_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, user_repeat_send_done_url, status_code=302, target_status_code=200)

        # self.assertEqual(user.email, user_repeat_send_data['email'])
