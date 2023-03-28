
from accounts.views import UserLoginView
from accounts.views import UserLogoutView
from accounts.views import UserProfileUpdateView
from accounts.views import UserRegisterView
from accounts.views import UserRepeatSendView
from accounts.views import user_activate
from accounts.views import user_profile_view

from django.test import SimpleTestCase
from django.views.generic import TemplateView
from django.urls import resolve
from django.urls import reverse


class TestUrls(SimpleTestCase):

    def test_register_url_resolves(self):
        url = reverse('accounts:register')  # вызываем маршрут
        # с помощью .func спрашиваем кто у resolve(url) является контроллером ,
        # если обрабатывается классом то вызываем дополнительно .view_class
        # если вызываем объект класса то self
        self.assertEqual(resolve(url).func.view_class, UserRegisterView)
        # assert resolve(url).func.view_class == UserRegisterView, 'Incorrect class'

    def test_profile_url_resolves(self):
        url = reverse('accounts:profile')
        self.assertEqual(resolve(url).func, user_profile_view)

    def test_activate_user_url_resolves(self):
        url = reverse('accounts:register_activate', kwargs={'sign': 'ioewutrljc3409ur90u43ri3j4'})
        self.assertEqual(resolve(url).func, user_activate)

    def test_register_done_url_resolves(self):
        url = reverse('accounts:register_done')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_email_done_url_resolves(self):
        url = reverse('accounts:email_done')
        self.assertEqual(resolve(url).func.view_class, TemplateView)

    def test_login_url_resolves(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, UserLoginView)

    def test_logout_url_resolves(self):
        url = reverse('accounts:logout')
        self.assertEqual(resolve(url).func.view_class, UserLogoutView)

    def test_resend_url_resolves(self):
        url = reverse('accounts:resend')
        self.assertEqual(resolve(url).func.view_class, UserRepeatSendView)

    def test_profile_update_url_resolves(self):
        url = reverse('accounts:profile_update')
        self.assertEqual(resolve(url).func.view_class, UserProfileUpdateView)
