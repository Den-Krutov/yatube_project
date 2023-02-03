from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class UrlsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.urls = ['/about/author/', '/about/tech/']

    def test_accepted_urls(self):
        for url in UrlsTest.urls:
            with self.subTest(url=url):
                responce = UrlsTest.guest_client.get(url)
                self.assertEqual(responce.status_code, HTTPStatus.OK)

    def test_urls_responce_correct_templates(self):
        templates = ['about/author.html', 'about/tech.html']
        url_templates = {
            url: template for url, template in zip(
                UrlsTest.urls, templates
            )
        }
        for url, template in url_templates.items():
            with self.subTest(url=url):
                responce = UrlsTest.guest_client.get(url)
                self.assertTemplateUsed(responce, template)


class ViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_urls_responce_correct_templates(self):
        templates = {
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
        }
        for url, template in templates.items():
            with self.subTest(url=url):
                responce = UrlsTest.guest_client.get(url)
                self.assertTemplateUsed(responce, template)
