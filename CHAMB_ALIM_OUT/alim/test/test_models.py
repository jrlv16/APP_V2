from django.test import TestCase
from django.contrib.auth import get_user_model
from alim import models


def sample_user(
    email='jl062705@sfr.fr',
    password='testpass',
):
    """
    Create a sample user
    """
    return get_user_model().objects.create_user(
        email,
        password,
    )


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user is successful"""
        clientcode = 'testuser'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            clientcode=clientcode,
            password=password
        )

        self.assertEqual(user.clientcode, clientcode)
        self.assertTrue(user.check_password(password))

    def test_create_new_superuser(self):
        """
        Test creating a new superuser
        """
        clientcode = 'jl062705'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            clientcode=clientcode,
            password=password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_cat(self):
        """
        Test the cat string representation
        """
        categorie = 'CLIENT'
        cat = models.Cat.objects.create(
            user=sample_user(),
            cat=categorie)

        self.assertEqual(cat.cat, categorie)
