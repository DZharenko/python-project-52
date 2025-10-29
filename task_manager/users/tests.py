# from django.contrib.auth import get_user_model
# from django.test import Client, TestCase
# from django.urls import reverse

# User = get_user_model()


# class UserCRUDTest(TestCase):
#     def setUp(self):
#         """Настройка тестовых данных"""
#         self.client = Client()
        
#         # Создаем тестового пользователя
#         self.user_data = {
#             'username': 'testuser',
#             'first_name': 'Test',
#             'last_name': 'User',
#             'email': 'test@example.com',
#             'password': 'testpass123'
#         }
#         self.user = User.objects.create_user(**self.user_data)
        
#         # Данные для нового пользователя
#         self.new_user_data = {
#             'first_name': 'New',
#             'last_name': 'User',
#             'username': 'newuser',
#             'email': 'new@example.com',
#             'password1': 'newpass123',
#             'password2': 'newpass123'
#         }

#     def test_user_create_view_get(self):
#         """Тест отображения формы регистрации (GET)"""
#         response = self.client.get(reverse('user_create'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/create.html')
#         # Проверяем наличие формы вместо конкретного текста
#         self.assertContains(response, '<form')
#         self.assertContains(response, 'csrfmiddlewaretoken')

#     def test_user_create_success(self):
#         """Тест успешной регистрации пользователя (C - Create)"""
#         response = self.client.post(reverse('user_create'), self.new_user_data)
        
#         # Проверяем редирект на страницу входа
#         self.assertRedirects(response, reverse('login'))
        
#         # Проверяем что пользователь создан в базе
#         self.assertTrue(User.objects.filter(username='newuser').exists())

#     def test_user_create_invalid_data(self):
#         """Тест регистрации с невалидными данными"""
#         invalid_data = self.new_user_data.copy()
#         invalid_data['password2'] = 'differentpassword'
        
#         response = self.client.post(reverse('user_create'), invalid_data)
        
#         # Должен остаться на той же странице с ошибками
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/create.html')
        
#         # Проверяем что пользователь не создан
#         self.assertFalse(User.objects.filter(username='newuser').exists())

#     def test_user_update_view_get_authenticated(self):
#         """Тест отображения формы редактирования для авторизованного пользователя"""
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('user_update', args=[self.user.id]))
        
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/update.html')
#         # Проверяем наличие формы и данных пользователя
#         self.assertContains(response, '<form')
#         self.assertContains(response, 'Test')  # имя пользователя
#         self.assertContains(response, 'testuser')  # username

#     def test_user_update_view_get_unauthenticated(self):
#         """Тест доступа к форме редактирования без авторизации"""
#         response = self.client.get(reverse('user_update', args=[self.user.id]))
        
#         # Должен редиректить на страницу пользователей
#         self.assertRedirects(response, reverse('users'))

#     def test_user_update_success(self):
#         """Тест успешного обновления пользователя (U - Update)"""
#         self.client.force_login(self.user)
        
#         updated_data = {
#             'first_name': 'Updated',
#             'last_name': 'Name',
#             'username': 'updateduser',
#             'email': 'updated@example.com'
#         }
        
#         response = self.client.post(
#             reverse('user_update', args=[self.user.id]),
#             updated_data
#         )
        
#         # Проверяем редирект на список пользователей
#         self.assertRedirects(response, reverse('users'))
        
#         # Обновляем данные пользователя из базы
#         self.user.refresh_from_db()
        
#         # Проверяем что данные обновились
#         self.assertEqual(self.user.first_name, 'Updated')
#         self.assertEqual(self.user.username, 'updateduser')

#     def test_user_update_other_user(self):
#         """Тест попытки редактирования чужого профиля"""
#         # Создаем второго пользователя
#         other_user = User.objects.create_user(
#             username='otheruser',
#             first_name='Other',
#             last_name='User',
#             email='other@example.com',
#             password='otherpass123'
#         )
        
#         # Логинимся как первый пользователь
#         self.client.force_login(self.user)
        
#         # Пытаемся редактировать второго пользователя
#         response = self.client.get(reverse('user_update', args=[other_user.id]))
        
#         # Должен редиректить на список пользователей с ошибкой
#         self.assertRedirects(response, reverse('users'))

#     def test_user_delete_view_get_authenticated(self):
#         """Тест отображения формы удаления для авторизованного пользователя (GET)"""
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('user_delete', args=[self.user.id]))
        
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/delete.html')
#         # Проверяем наличие формы и имени пользователя
#         self.assertContains(response, '<form')
#         self.assertContains(response, 'Test User')

#     def test_user_delete_success(self):
#         """Тест успешного удаления пользователя (D - Delete)"""
#         self.client.force_login(self.user)
        
#         user_id = self.user.id
#         response = self.client.post(reverse('user_delete', args=[user_id]))
        
#         # Проверяем редирект на список пользователей
#         self.assertRedirects(response, reverse('users'))
        
#         # Проверяем что пользователь удален из базы
#         self.assertFalse(User.objects.filter(id=user_id).exists())

#     def test_user_delete_other_user(self):
#         """Тест попытки удаления чужого профиля"""
#         # Создаем второго пользователя
#         other_user = User.objects.create_user(
#             username='otheruser',
#             first_name='Other',
#             last_name='User',
#             email='other@example.com',
#             password='otherpass123'
#         )
        
#         # Логинимся как первый пользователь
#         self.client.force_login(self.user)
        
#         # Пытаемся удалить второго пользователя
#         response = self.client.get(reverse('user_delete', args=[other_user.id]))
        
#         # Должен редиректить на список пользователей с ошибкой
#         self.assertRedirects(response, reverse('users'))
        
#         # Проверяем что второй пользователь не удален
#         self.assertTrue(User.objects.filter(id=other_user.id).exists())

#     def test_user_list_view(self):
#         """Тест отображения списка пользователей"""
#         response = self.client.get(reverse('users'))
        
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'users/index.html')
#         # Проверяем наличие таблицы и данных пользователя
#         self.assertContains(response, '<table')
#         self.assertContains(response, 'testuser')
        
#         # Проверяем что пользователь есть в контексте
#         self.assertIn('users', response.context)
#         self.assertEqual(len(response.context['users']), 1)


# class UserAuthenticationTest(TestCase):
#     """Тесты аутентификации"""
    
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass123'
#         )
    
#     def test_login_view_get(self):
#         """Тест отображения формы входа"""
#         response = self.client.get(reverse('login'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login.html')
#         # Проверяем наличие формы входа
#         self.assertContains(response, '<form')
#         self.assertContains(response, 'username')
#         self.assertContains(response, 'password')
    
#     def test_login_success(self):
#         """Тест успешного входа"""
#         response = self.client.post(reverse('login'), {
#             'username': 'testuser',
#             'password': 'testpass123'
#         })
        
#         self.assertRedirects(response, reverse('home'))
    
#     def test_login_failure(self):
#         """Тест неудачного входа"""
#         response = self.client.post(reverse('login'), {
#             'username': 'testuser',
#             'password': 'wrongpassword'
#         })
        
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'login.html')
    
#     def test_logout(self):
#         """Тест выхода из системы"""
#         self.client.force_login(self.user)
        
#         # Проверяем что пользователь авторизован
#         self.assertTrue(self.user.is_authenticated)
        
#         response = self.client.get(reverse('logout'))
        
#         self.assertRedirects(response, reverse('home'))


# class UserAccessTest(TestCase):
#     """Тесты доступа к страницам"""
    
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass123'
#         )
    
#     def test_public_pages_access(self):
#         """Тест доступа к публичным страницам без авторизации"""
#         public_urls = [
#             reverse('home'),
#             reverse('users'),
#             reverse('login'),
#             reverse('user_create'),
#         ]
        
#         for url in public_urls:
#             response = self.client.get(url)
#             self.assertEqual(response.status_code, 200,
#                            f"Страница {url} должна быть доступна без авторизации")
    
#     def test_protected_pages_redirect_when_anonymous(self):
#         """Тест что защищенные страницы редиректят анонимных пользователей"""
#         protected_urls = [
#             reverse('user_update', args=[1]),
#             reverse('user_delete', args=[1]),
#             reverse('logout'),
#         ]
        
#         for url in protected_urls:
#             response = self.client.get(url)
#             self.assertNotEqual(response.status_code, 200,
#                               f"Страница {url} не должна быть доступна без авторизации")


# class UserFunctionalityTest(TestCase):
#     """Тесты функциональности пользователей"""
    
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='testuser',
#             first_name='Test',
#             last_name='User',
#             email='test@example.com',
#             password='testpass123'
#         )
    
#     def test_user_full_name(self):
#         """Тест метода get_full_name"""
#         self.assertEqual(self.user.get_full_name(), 'Test User')
    
#     def test_user_str_representation(self):
#         """Тест строкового представления пользователя"""
#         self.assertEqual(str(self.user), 'Test User')
    
#     def test_user_creation_count(self):
#         """Тест что пользователи создаются правильно"""
#         initial_count = User.objects.count()
        
#         # Создаем нового пользователя
#         new_user = User.objects.create_user(
#             username='newuser',
#             first_name='New',
#             last_name='User',
#             email='new@example.com',
#             password='newpass123'
#         )
        
#         self.assertEqual(User.objects.count(), initial_count + 1)
#         self.assertEqual(new_user.get_full_name(), 'New User')
import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.db.models import ProtectedError

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

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

    #     # Проверяем редирект на страницу логина
    #     self.assertRedirects(response, reverse('login'))
    #     self.assertEqual(User.objects.count(), initial_users + 1)
    #     self.assertTrue(User.objects.filter(username='newuser').exists())

    #     messages = list(get_messages(response.wsgi_request))
    #     assert any("успешно" in str(m).lower() for m in messages)

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

    #     # Проверяем редирект на страницу списка пользователей
    #     self.assertRedirects(response, reverse('users'))
    #     self.user1.refresh_from_db()
    #     self.assertEqual(self.user1.first_name, 'Updated')
    #     self.assertTrue(self.user1.check_password('newpass123'))

    # def test_user_update_unauthenticated(self):
    #     url = reverse('user_update', kwargs={'pk': self.user1.pk})
    #     response = self.client.post(url)

    #     login_url = reverse('login')
    #     expected_redirect = f"{login_url}?next={url}"
    #     self.assertRedirects(response, expected_redirect)

    #     messages = list(get_messages(response.wsgi_request))
    #     assert any("не авторизованы" in str(m).lower() for m in messages)

    def test_user_update_other_user(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('user_update', kwargs={'pk': self.user2.pk})
        response = self.client.post(url, {
            'username': 'user2',
            'first_name': 'Hacked',
            'last_name': 'User',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        # Проверяем, что чужой пользователь не обновился
        self.user2.refresh_from_db()
        self.assertNotEqual(self.user2.first_name, 'Hacked')

    def test_cannot_delete_user_with_tasks(self):
        status = Status.objects.create(name='В работе')
        Task.objects.create(
            name="Test task",
            status=status,
            author=self.user1
        )

        self.client.login(username='user1', password='testpass123')
        url = reverse('user_delete', kwargs={'pk': self.user1.pk})
        with self.assertRaises(ProtectedError):
            self.client.post(url)

    def test_user_delete_success(self):
        self.client.login(username='user3', password='testpass123')
        url = reverse('user_delete', kwargs={'pk': self.user3.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users'))
        self.assertFalse(User.objects.filter(pk=self.user3.pk).exists())

    def test_user_list_view(self):
        self.client.login(username='user1', password='testpass123')
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)
        self.assertContains(response, self.user3.username)


@pytest.mark.django_db
class UserAccessTest(TestCase):
    fixtures = ['users.json']

    def test_public_pages_access(self):
        urls = [
            reverse('users'),
            reverse('user_create'),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertIn(response.status_code, [200, 302])