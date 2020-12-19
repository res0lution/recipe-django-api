from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        admin_email = "testadmin@email.com"
        admin_password = "admintestpassword123"
        email = "test@email.com"
        password = "usertestpassword123"
        self.admin_user = get_user_model().objects.create_superuser(
            email=admin_email,
            password=admin_password
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name="testusername"
        )
    
    def test_user_listed(self):
        """Test that users are listed on users page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)


