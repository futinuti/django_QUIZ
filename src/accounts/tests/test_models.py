from accounts.models import User

from django.test import TestCase


class TestModels(TestCase):
    username = None

    # 2 метода для предварительной настройки
    #

    @classmethod
    def setUpTestData(cls):  # этот запускается один раз
        cls.username = 'user_1'  # объявляется атрибут класса

        User.objects.create(
            username=cls.username,
            password='123qwe!@#',
            email='user_1@test.com',
            first_name='Test'
        )

    # этот метод будет запускаться перед каждым запуском тестов

    def setUp(self):
        self.user = User.objects.get(username=self.username)

    def test_avatar_label_is_correct(self):
        avatar_label = self.user._meta.get_field('avatar').verbose_name
        self.assertEqual(avatar_label, 'avatar')

    def test_city_max_length(self):
        meta = self.user._meta.get_field('city')
        self.assertEqual(meta.max_length, 50)
        self.assertTrue(meta.null)
        self.assertTrue(meta.blank)

    def test_convert_user_to_str(self):
        self.assertEqual(str(self.user), self.username)

    def test_birthday_null(self):
        meta = self.user._meta.get_field('birthday')
        self.assertTrue(meta.null)

    def test_birthday_blank(self):
        meta = self.user._meta.get_field('birthday')
        self.assertTrue(meta.blank)

    def test_is_activated_default(self):
        meta = self.user._meta.get_field('is_activated')
        self.assertTrue(meta.default)

    def test_is_activated_db_index(self):
        meta = self.user._meta.get_field('is_activated')
        self.assertTrue(meta.db_index)

    def test_is_activated_label_is_correct(self):
        is_activated_label = self.user._meta.get_field('is_activated').verbose_name
        self.assertEqual(is_activated_label.split(), 'is_activated'.split('_'))

    def test_birthday_label_is_correct(self):
        birthday_label = self.user._meta.get_field('birthday').verbose_name
        self.assertEqual(birthday_label, 'birthday')

    def test_city_label_is_correct(self):
        city_label = self.user._meta.get_field('city').verbose_name
        self.assertEqual(city_label, 'city')
