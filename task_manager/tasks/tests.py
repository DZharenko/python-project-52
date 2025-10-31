from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

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
            reverse('task_create'),
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
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_task_list_requires_login(self):
        """Тест что список задач требует авторизации"""
        response = self.client.get(reverse('tasks_index'))
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
            reverse('task_detail', kwargs={'pk': task.pk})
        )
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
            reverse('task_update', kwargs={'pk': task.pk})
        )
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
        
        self.client.login(username='user2', password='password123')
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())
        
        self.client.login(username='user1', password='password123')
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.pk})
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
        response = self.client.get(reverse('tasks_index'))
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
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('task_create'),
            data=self.task_data
        )
        self.assertEqual(response.status_code, 302)
        task = Task.objects.get(name='Integration Test Task')
        
        response = self.client.get(reverse('tasks_index'))
        self.assertContains(response, 'Integration Test Task')
        
        response = self.client.get(
            reverse('task_detail', kwargs={'pk': task.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Integration Test Task')
        
        update_data = {
            'name': 'Updated Task Name',
            'description': 'Updated description',
            'status': self.status.id,
        }
        response = self.client.post(
            reverse('task_update', kwargs={'pk': task.pk}),
            data=update_data
        )
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Task Name')
        
        response = self.client.post(
            reverse('task_delete', kwargs={'pk': task.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())


class TaskFilterTest(TestCase):
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
        
        self.status_new = Status.objects.create(name='New')
        self.status_in_progress = Status.objects.create(name='In Progress')
        
        self.label_bug = Label.objects.create(name='Bug')
        self.label_feature = Label.objects.create(name='Feature')
        
        self.task1 = Task.objects.create(
            name='Task 1',
            description='Description 1',
            status=self.status_new,
            author=self.user1,
            executor=self.user2
        )
        self.task1.labels.add(self.label_bug)
        
        self.task2 = Task.objects.create(
            name='Task 2',
            description='Description 2',
            status=self.status_in_progress,
            author=self.user2,
            executor=self.user1
        )
        self.task2.labels.add(self.label_feature)
        
        self.task3 = Task.objects.create(
            name='Task 3',
            description='Description 3',
            status=self.status_new,
            author=self.user1,
            executor=None
        )
        self.task3.labels.add(self.label_bug, self.label_feature)

    def test_filter_by_status(self):
        """Тест фильтрации по статусу"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(
            reverse('tasks_index') + '?status=' + str(self.status_new.id)
            )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_executor(self):
        """Тест фильтрации по исполнителю"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(
            reverse('tasks_index') + '?executor=' + str(self.user2.id)
            )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 3')

    def test_filter_by_label(self):
        """Тест фильтрации по метке"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(
            reverse('tasks_index') + '?labels=' + str(self.label_bug.id)
            )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertContains(response, 'Task 3')

    def test_filter_self_tasks(self):
        """Тест фильтрации только своих задач"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse('tasks_index') + '?self_tasks=on')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')
        self.assertContains(response, 'Task 3')

    def test_combined_filter(self):
        """Тест комбинированной фильтрации"""
        self.client.login(username='user1', password='password123')
        
        url = (
            reverse('tasks_index') + 
            f'?status={self.status_new.id}&labels={self.label_bug.id}'
        )
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 3')
        self.assertNotContains(response, 'Task 2')

    def test_empty_filter_results(self):
        """Тест пустых результатов фильтрации"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse('tasks_index') + '?status=999')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, _('No tasks found'))

    def test_filter_form_displayed(self):
        """Тест что форма фильтрации отображается"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse('tasks_index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id_status')
        self.assertContains(response, 'id_executor')
        self.assertContains(response, 'id_labels')
        self.assertContains(response, 'id_self_tasks')
        self.assertContains(response, 'btn-primary')