import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
class UserCRUDTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)

        for user in [self.user1, self.user2, self.user3]:
            user.set_password('testpass123')
            user.save()

    # def test_user_registration(self):
    #     initial_users = User.objects.count()

    #     url = reverse('user_create')
    #     data = {
    #         'username': 'newuser',
    #         'password1': 'newpass123',
    #         'password2': 'newpass123',
    #         'first_name': 'New',
    #         'last_name': 'User'
    #     }
    #     response = self.client.post(url, data)

    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(User.objects.count(), initial_users + 1)
    #     self.assertTrue(User.objects.filter(username='newuser').exists())

    #     messages = list(get_messages(response.wsgi_request))
    #     assert "успешно" in str(messages[0]).lower()

    # def test_user_update_authenticated(self):
    #     self.client.login(username='user1', password='testpass123')
    #     url = reverse('user_update', kwargs={'pk': self.user1.pk})
    #     response = self.client.post(
    #         url,
    #         {
    #             'username': 'user1',
    #             'first_name': 'Updated',
    #             'last_name': 'User',
    #             'password1': 'newpass123',
    #             'password2': 'newpass123',
    #         }
    #     )
    #     self.assertRedirects(response, reverse('users'))
    #     self.user1.refresh_from_db()
    #     self.assertEqual(self.user1.first_name, 'Updated')
    #     self.assertTrue(self.user1.check_password('newpass123'))

    def test_user_update_unauthenticated(self):
        url = reverse('user_update', kwargs={'pk': self.user1.pk})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('users'))

    def test_user_delete_success(self):
        self.client.login(username='user1', password='testpass123')
        
        user_id = self.user1.id
        response = self.client.post(reverse('user_delete', args=[user_id]))
        
        self.assertRedirects(response, reverse('users'))
        self.assertFalse(User.objects.filter(id=user_id).exists())

    def test_user_delete_other_user(self):
        self.client.login(username='user1', password='testpass123')
        
        response = self.client.get(reverse('user_delete', args=[self.user2.id]))
        
        self.assertRedirects(response, reverse('users'))
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())