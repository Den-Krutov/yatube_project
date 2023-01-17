from django.test import Client, TestCase


class StaticUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.noauth_client = Client()

    def test_homepage(self):
        responce = StaticUrlTests.noauth_client.get('/')
        self.assertEqual(responce.status_code, 200)
