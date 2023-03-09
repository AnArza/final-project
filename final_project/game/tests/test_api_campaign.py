import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import Campaign


class MyAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.my_object = Campaign.objects.create(name='test object', budget=12)
        self.url = reverse('campaign')
        self.url_detailed = reverse('campaign_id', args=[1])

    def test_get_api(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_content = json.loads(
            '{"data": [{"id": 1, "name": "test object", "budget": 12}], "status": "ok"}')

        self.assertJSONEqual(response.json(), expected_content)

    def test_get_id_api(self):
        response = self.client.get(self.url_detailed)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_content = json.loads(
            '{"data": {"id": 1, "name": "test object", "budget": 12}, "status": "ok"}')

        self.assertJSONEqual(response.json(), expected_content)

    def test_post_api(self):
        # response = self.client.create(name='test object', budget=12)
        data = {"name": "test object", "budget": 12}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_post_no_data_api(self):
        # response = self.client.create(name='test object', budget=12)
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 404)
        # self.assertEqual(Campaign.objects.count(), 0)

    # def test_delete_api(self):
    #     response = self.client.delete(self.url_detailed, json.loads('{"id": 1}'))
    #     self.assertEqual(response.status_code, 200)

    # def test_edit_api(self):
    #     data = {"name": "Updated Object"}
    #     response = self.client.put(self.url_detailed, data, format='json')
    #     print(response.json())
    #     self.assertEqual(response.status_code, 200)
