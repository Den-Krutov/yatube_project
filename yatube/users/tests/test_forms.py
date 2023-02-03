from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class FormsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup(self):
        users_count = User.objects.count()
        form_data = {
            'first_name': 'test first name',
            'last_name': 'test last name',
            'username': 'test_username',
            'email': 'xxxxxx@yandex.com',
            'password1': 'asdfjkl;1',
            'password2': 'asdfjkl;1',
        }
        response = self.client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:index')
        )
        self.assertEqual(User.objects.count(), users_count + 1)
