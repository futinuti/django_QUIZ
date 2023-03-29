from accounts.forms import UserRegisterForm, UserRepeatSend, UserUpdateForm

from django.test import TestCase


class TestForms(TestCase):
    def setUp(self):
        self.username = 'user_1'
        self.password = '123qwe!@#'
        self.email = 'user_1@test.com'
        self.birthday = '2008-08-08'
        self.city = 'city'
        self.avatar = 'profile/default.png'

    def test_register_form_valid_data(self):
        # передаем параметры в форму
        form = UserRegisterForm(
            data={
                'username': self.username,
                'email': self.email,
                'password1': self.password,
                'password2': self.password
            }
        )

        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_user_repeat_form_valid_data(self):
        form = UserRepeatSend(
            data={
                'email': self.email,
            }
        )

        self.assertTrue(form.is_valid())

    def test_user_repeat_form_no_data(self):
        form = UserRepeatSend(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_user_update_form_valid_data(self):
        first_name = 'First'
        last_name = 'Last'
        form = UserUpdateForm(
            data={
                'username': self.username,
                'email': self.email,
                'first_name': first_name,
                'last_name': last_name,
                'birthday': self.birthday,
                'city': self.city,
                'avatar': self.avatar,
            }
        )

        self.assertTrue(form.is_valid())
