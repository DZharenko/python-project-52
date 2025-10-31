from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label

User = get_user_model()


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.label_data = {
            'name': 'Test Label'
        }

    def test_label_creation(self):
        """Тест создания метки"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('label_create'),
            data=self.label_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Test Label').exists())

    def test_label_creation_requires_login(self):
        """Тест что создание метки требует авторизации"""
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_label_list_requires_login(self):
        """Тест что список меток требует авторизации"""
        response = self.client.get(reverse('labels_index'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_label_update_requires_login(self):
        """Тест что редактирование метки требует авторизации"""
        label = Label.objects.create(name='Test Label')
        response = self.client.get(
            reverse('label_update', kwargs={'pk': label.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_label_delete_requires_login(self):
        """Тест что удаление метки требует авторизации"""
        label = Label.objects.create(name='Test Label')
        response = self.client.get(
            reverse('label_delete', kwargs={'pk': label.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_label_fields(self):
        """Тест полей метки"""
        label = Label.objects.create(name='Test Label')
        self.assertEqual(str(label), 'Test Label')
        self.assertEqual(label.name, 'Test Label')


class LabelIntegrationTest(TestCase):
    """Интеграционные тесты для меток"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_full_label_lifecycle(self):
        """Полный цикл: создание -> редактирование -> удаление"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('label_create'),
            data={'name': 'Test Label'}
        )
        self.assertEqual(response.status_code, 302)
        label = Label.objects.get(name='Test Label')
        
        response = self.client.get(reverse('labels_index'))
        self.assertContains(response, 'Test Label')
        
        response = self.client.post(
            reverse('label_update', kwargs={'pk': label.pk}),
            data={'name': 'Updated Label'}
        )
        self.assertEqual(response.status_code, 302)
        label.refresh_from_db()
        self.assertEqual(label.name, 'Updated Label')
        
        response = self.client.post(
            reverse('label_delete', kwargs={'pk': label.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=label.pk).exists())