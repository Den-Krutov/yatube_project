from http import HTTPStatus

from django.test import Client, TestCase


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pages_error_uses_correct_templates(self):
        response = self.client.get('/unexcepting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')
