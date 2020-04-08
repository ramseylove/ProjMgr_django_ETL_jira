from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve


class CustomUserTest(TestCase):

    def test_create_user(self):
        user = get_user_model()
        user = user.objects.create_user(
            username='ryguy',
            email='meyeryan@gmail.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'ryguy')
        self.assertEqual(user.email, 'meyeryan@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin', 
            email='superadmin@email.com',
            password='testpass212'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
