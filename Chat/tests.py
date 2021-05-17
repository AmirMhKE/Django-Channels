from django.test import TestCase
from account.models import User

class RegistrationTestCase(TestCase):
    def setUp(self):
        User.objects.create(username="amke", password="amir8531")
        User.objects.create(username="aMke", password="amir8531")
        User.objects.create(username="aMkE", password="amir8531")
        User.objects.create(username="aMkE1", password="amir8531")
        User.objects.create(username="aMkE2", password="amir8531")
        User.objects.create(username="aMkE3", password="amir8531")

    def find_users(self):
        self.assertEqual(User.objects.filter(username__iexact="amke")[0].username, "amke")