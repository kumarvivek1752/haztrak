import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.trak.models import Manifest, Site


class TrakViewsTest(TestCase):
    fixtures = ['site_handler_manifest.json']

    # SetUpTestData() runs once per Test Class, setUp() runs each before method
    @classmethod
    def setUpTestData(cls):
        try:
            User.objects.create_user(username='username', password='password')
            cls.manifest_mtn = Manifest.objects.filter(mtn='000000001ELC').get()
            cls.site = Site.objects.filter(id=1).get()
        except ObjectDoesNotExist:
            logging.error('object does not exist')
        except IntegrityError:
            logging.error('integrity error')

    def setUp(self) -> None:
        self.client.login(username='username', password='password')

    # Test that these urls return 200 with logged in user
    def test_trak_url_exists(self):
        response = self.client.get('/trak/')
        self.assertEqual(response.status_code, 200)

    def test_manifest_view_exists(self):
        response = self.client.get(f'/trak/manifest/{self.manifest_mtn.id}')
        self.assertEqual(response.status_code, 200)

    def test_site_details_view_exists(self):
        response = self.client.get(f'/trak/{self.site.id}/details')
        self.assertEqual(response.status_code, 200)

    # Test that these URLs redirect to login page if user is logged out
    def test_trak_url_redirect_without_login(self):
        self.client.logout()
        response = self.client.get(f'/trak/{self.site.id}/details')
        self.assertEqual(response.status_code, 302)

    def test_manifest_view_redirects_without_login(self):
        self.client.logout()
        response = self.client.get(f'/trak/manifest/{self.manifest_mtn.id}',
                                   follow=False)
        self.assertEqual(response.status_code, 302)

    def test_site_details_view_redirects_without_login(self):
        self.client.logout()
        response = self.client.get(f'/trak/{self.site.id}/details',
                                   follow=False)
        self.assertEqual(response.status_code, 302)

    # Test non-existent model objects return 404
    def test_non_exist_mtn_view_returns_404(self):
        mtn_count = Manifest.objects.all().count()
        response = self.client.get(f'/trak/manifest/'
                                   f'{mtn_count + 128}')
        self.assertEqual(response.status_code, 404)

    def test_non_exist_site_view_returns_404(self):
        site_count = Site.objects.all().count()
        response = self.client.get(f'/trak/{site_count + 128}ELC/details')
        self.assertEqual(response.status_code, 404)
