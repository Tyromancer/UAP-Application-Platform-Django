from django.test import TestCase, Client
from django.urls import reverse
from post.models import URP, Application
import json


class TestViews(TestCase):
    """Test if views work correctly
    """

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('uap-home')
        self.about_url = reverse('uap-about')
        self.detail_url = reverse('urp-detail', args=['1'])

    def test_home_page_GET(self):
        response = self.client.get(self.home_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/home.html')

    def test_about_page_GET(self):
        response = self.client.get(self.about_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/about.html')

    # def test_detail_page_GET(self):
    #     # TODO: create mock object of URP for testing
    #     print(self.detail_url)
    #     response = self.client.get(self.detail_url)

    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'post/urp_detail.html')

    