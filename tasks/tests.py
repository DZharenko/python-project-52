from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Task
from statuses.models import Status

User = get_user_model()


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            password='password123',
            first_name='Jane',
            last_name='Smith'
        )
        self.status = Status.objects.create(name='Test Status')
        self.task_data = {
            'name': 'Test Task',
            'description': 'Test Description',
            'status': self.status.id,
            'executor': self.user2.id,
        }

    def test_task_creation(self):
        """Тест создания задачи"""
        self.client.login(username='user1', password='password123')
        response = self.client.post(
            reverse('tasks:task_create'),
            data=self.task_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Test Task').exists())
        
        task = Task.objects.get(name='Test Task')
        self.assertEqual(task.author, self.user1)
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.executor, self.user2)

    def test_task_creation_requires_login(self):
        """Тест что создание задачи требует авторизации"""
        response = self.client.get(reverse('tasks:task_create'))
        # Проверяем редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_task_list_requires_login(self):
        """Тест что список задач требует авторизации"""
        response = self.client.get(reverse('tasks:tasks'))
        # Проверяем редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_task_detail_requires_login(self):
        """Тест что просмотр задачи требует авторизации"""
        task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user1
        )
        response = self.client.get(
            reverse('tasks:task_detail', kwargs={'pk': task.pk})
        )
        # Проверяем редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_task_update_requires_login(self):
        """Тест что редактирование задачи требует авторизации"""
        task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user1
        )
        response = self.client.get(
            reverse('tasks:task_update', kwargs={'pk': task.pk})
        )
        # Проверяем редирект на страницу логина
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_task_delete_only_by_author(self):
        """Тест что удалять задачу может только автор"""
        task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user1
        )
        
        # Пользователь user2 пытается удалить задачу
        self.client.login(username='user2', password='password123')
        response = self.client.post(
            reverse('tasks:task_delete', kwargs={'pk': task.pk})
        )
        # Должен быть редирект с сообщением об ошибке
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        
        # Автор удаляет задачу
        self.client.login(username='user1', password='password123')
        response = self.client.post(
            reverse('tasks:task_delete', kwargs={'pk': task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_task_fields(self):
        """Тест полей задачи"""
        task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user1,
            executor=self.user2
        )
        self.assertEqual(str(task), 'Test Task')
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.author, self.user1)
        self.assertEqual(task.executor, self.user2)


class TaskListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description', 
            status=self.status,
            author=self.user
        )

    def test_task_list_view(self):
        """Тест отображения списка задач"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tasks:tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertContains(response, 'Test Task')


class TaskIntegrationTest(TestCase):
    """Интеграционные тесты для полного цикла CRUD"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.status = Status.objects.create(name='In Progress')
        self.task_data = {
            'name': 'Integration Test Task',
            'description': 'This is a test task for integration testing',
            'status': self.status.id,
        }

    def test_full_task_lifecycle(self):
        """Полный цикл: создание -> просмотр -> редактирование -> удаление"""
        # Логинимся
        self.client.login(username='testuser', password='testpass123')
        
        # 1. Создаем задачу
        response = self.client.post(
            reverse('tasks:task_create'),
            data=self.task_data
        )
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(name='Integration Test Task')
        
        # 2. Проверяем что задача в списке
        response = self.client.get(reverse('tasks:tasks'))
        self.assertContains(response, 'Integration Test Task')
        
        # 3. Просматриваем задачу
        response = self.client.get(
            reverse('tasks:task_detail', kwargs={'pk': task.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration Test Task')
        
        # 4. Редактируем задачу
        update_data = {
            'name': 'Updated Task Name',
            'description': 'Updated description',
            'status': self.status.id,
        }
        response = self.client.post(
            reverse('tasks:task_update', kwargs={'pk': task.pk}),
            data=update_data
        )
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Task Name')
        
        # 5. Удаляем задачу
        response = self.client.post(
            reverse('tasks:task_delete', kwargs={'pk': task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())