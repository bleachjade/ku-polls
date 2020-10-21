from django.test import TestCase
from django.contrib.auth.models import User
from polls.views import *


class AuthTest(TestCase):
    """Test authentication in polls app."""

    def setUp(self):
        """Set up value to test."""
        self.credentials = {
            'username': 'test',
            'password': 'password'}
        User.objects.create_user(**self.credentials)

    def test_display_login_page(self):
        """Test displaying login page."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(redirect('login'))

    def test_login(self):
        """Test login procedure."""
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertTemplateUsed(redirect('polls:index'))

    def test_logout(self):
        """Test logout by logging-in first."""
        # login
        response = self.client.post(reverse('login'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_active)
        self.assertTemplateUsed(redirect('polls:index'))
        # logout
        response = self.client.post(reverse('logout'), follow=True)
        self.assertFalse(response.context['user'].is_active)
        self.assertTemplateUsed(redirect('polls:index'))

    def test_wrong_login_info(self):
        """Test input wrong user login information."""
        response = self.client.post(reverse('login'), {
            'username': 'hacker',
            'password': 'f34cwx3'}, follow=True)
        self.assertFalse(response.context['user'].is_active)
