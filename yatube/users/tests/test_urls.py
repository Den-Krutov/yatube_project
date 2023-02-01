from http import HTTPStatus

from django.test import Client, TestCase

from posts.models import User


class UrlsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='authUser')
        urls = [
            'login/',
            'signup/',
            'password_change/',
            'password_change/done/',
            'password_reset/',
            'password_reset/done/',
            'reset/done/',
            'logout/',
        ]
        cls.urls = [
            '/auth/' + url for url in urls
        ]

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(UrlsTest.user)

    def test_accepted_urls(self):
        for url in UrlsTest.urls:
            with self.subTest(url=url):
                responce = self.auth_client.get(url)
                self.assertEqual(responce.status_code, HTTPStatus.OK)

    def test_urls_responce_correct_templates(self):
        templates_names = [
            'login',
            'signup',
            'password_change',
            'password_change_done',
            'password_reset',
            'password_reset_done',
            'password_reset_complete',
            'logout',
        ]
        template_paths = {
            url: f'users/{name}.html' for url, name in zip(
                UrlsTest.urls, templates_names
            )
        }
        for url, template in template_paths.items():
            with self.subTest(url=url):
                responce = self.auth_client.get(url)
                self.assertTemplateUsed(responce, template)
