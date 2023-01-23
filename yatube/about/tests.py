from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class AboutUrlsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_accepted_urls(self):
        url_patterns = [reverse('about:author'), reverse('about:tech')]
        for url in url_patterns:
            with self.subTest(url=url):
                responce = AboutUrlsTests.guest_client.get(url)
                self.assertEqual(responce.status_code, HTTPStatus.OK.value)

    def test_urls_responce_correct_templates(self):
        templates = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for url, template in templates.items():
            with self.subTest(url=url):
                responce = AboutUrlsTests.guest_client.get(url)
                self.assertTemplateUsed(responce, template)
