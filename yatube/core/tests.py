from http import HTTPStatus

from django.test import TestCase

from .models import CreateModel


class ModelsTest(TestCase):
    def test_verbose_name(self):
        expected = 'Дата создания'
        self.assertEqual(
            CreateModel._meta.get_field('created').verbose_name,
            expected
        )


class ViewsTest(TestCase):
    def test_pages_error_uses_correct_templates(self):
        response = self.client.get('/unexcepting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')
