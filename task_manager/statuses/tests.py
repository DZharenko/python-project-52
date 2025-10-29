from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.models import Status

User = get_user_model()


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.status_data = {
            'name': 'Test Status'
        }
        self.status = Status.objects.create(name='Existing Status')

    def test_status_list_view_authenticated(self):
        """Тест списка статусов для авторизованного пользователя"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')
        self.assertContains(response, '<table')

    def test_status_list_view_unauthenticated(self):
        """Тест что список статусов недоступен без авторизации"""
        response = self.client.get(reverse('statuses:statuses'))
        self.assertNotEqual(response.status_code, 200)

    def test_status_create_view_authenticated(self):
        """Тест создания статуса для авторизованного пользователя"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

    def test_status_create_success(self):
        """Тест успешного создания статуса"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:status_create'), self.status_data)
        self.assertRedirects(response, reverse('statuses:statuses'))
        self.assertTrue(Status.objects.filter(name='Test Status').exists())

    def test_status_update_view_authenticated(self):
        """Тест обновления статуса для авторизованного пользователя"""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('statuses:status_update', args=[self.status.id])
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

    def test_status_update_success(self):
        """Тест успешного обновления статуса"""
        self.client.force_login(self.user)
        updated_data = {'name': 'Updated Status'}
        response = self.client.post(
            reverse('statuses:status_update', args=[self.status.id]),
            updated_data
        )
        self.assertRedirects(response, reverse('statuses:statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete_view_authenticated(self):
        """Тест удаления статуса для авторизованного пользователя"""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('statuses:status_delete', args=[self.status.id])
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/delete.html')

    def test_status_delete_success(self):
        """Тест успешного удаления статуса"""
        self.client.force_login(self.user)
        status_id = self.status.id
        response = self.client.post(reverse('statuses:status_delete', args=[status_id]))
        self.assertRedirects(response, reverse('statuses:statuses'))
        self.assertFalse(Status.objects.filter(id=status_id).exists())


class StatusAccessTest(TestCase):
    """Тесты доступа к статусам"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.status = Status.objects.create(name='Test Status')

    def test_protected_pages_require_login(self):
        """Тест что защищенные страницы требуют авторизации"""
        protected_urls = [
            reverse('statuses:statuses'),
            reverse('statuses:status_create'),
            reverse('statuses:status_update', args=[1]),
            reverse('statuses:status_delete', args=[1]),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)
            
            self.client.force_login(self.user)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.client.logout()


class StatusModelTest(TestCase):
    """Тесты модели статуса"""
    
    def test_status_creation(self):
        """Тест создания статуса"""
        status = Status.objects.create(name='Test Status')
        self.assertEqual(str(status), 'Test Status')
        self.assertTrue(Status.objects.filter(name='Test Status').exists())

    def test_status_ordering(self):
        """Тест порядка статусов"""
        status1 = Status.objects.create(name='Status 1')
        status2 = Status.objects.create(name='Status 2')
        status3 = Status.objects.create(name='Status 3')
        
        statuses = Status.objects.all()
        self.assertEqual(statuses[0], status1)
        self.assertEqual(statuses[1], status2)
        self.assertEqual(statuses[2], status3)