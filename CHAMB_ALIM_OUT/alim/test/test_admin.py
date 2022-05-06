from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            clientcode="testadmin",
            password="test123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            clientcode="simpletestadmin",
            password="admin123",
            last_name="useradmintest"
        )

    def test_users_listed(self):
        """
        Test that users are listed on users page
        """
        url = reverse('admin:alim_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.last_name)
        self.assertContains(res, self.user.clientcode)

    def test_user_change_page(self):
        """
        Test that the user edit page works
        """
        url = reverse('admin:alim_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user(self):
        """
        Test that the creat user page works
        """
        url = reverse('admin:alim_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
