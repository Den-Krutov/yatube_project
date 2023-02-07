from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class FormsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form_data = {
            'first_name': 'test first name',
            'last_name': 'test last name',
            'username': 'test_username',
            'email': 'xxxxxx@yandex.com',
            'password1': 'asdfjkl;1',
            'password2': 'asdfjkl;1',
        }

    def test_signup(self):
        users_count = User.objects.count()
        response = self.client.post(
            reverse('users:signup'),
            data=FormsTest.form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:index')
        )
        self.assertEqual(User.objects.count(), users_count + 1)
