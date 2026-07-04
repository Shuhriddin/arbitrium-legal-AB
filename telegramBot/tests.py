from django.test import SimpleTestCase


class ApiUrlsTest(SimpleTestCase):
    def test_api_root_is_accessible(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
