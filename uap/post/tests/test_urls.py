from django.test import SimpleTestCase
from django.urls import reverse, resolve
from post.views import home, about, URPDetailView, URPCreateView


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        """Test if the url to the UAP home page resolves and links to the right view
        """

        url = reverse('uap-home')
        self.assertEquals(resolve(url).func, home)

    def test_about_url_is_resolved(self):
        """Test if the url to the UAP about page resolves and links to the right view
        """

        url = reverse('uap-about')
        self.assertEquals(resolve(url).func, about)

    def test_urp_detail_view_is_resolved(self):
        """Test if the url to the URP detail page resolves and links to the right view
        """

        url = reverse('urp-detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, URPDetailView)

    def test_urp_create_view_is_resolved(self):
        """Test if the url to the URP create page resolves and links to the right view
        """

        url = reverse('urp-create')
        self.assertEquals(resolve(url).func.view_class, URPCreateView)
