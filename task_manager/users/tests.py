from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserCRUDTest(TestCase):
    fixtures = ['users.json']  # Загружаем 3 пользователей из фикстуры
    
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        
        # Получаем пользователей из фикстуры
        self.users = User.objects.all()
        self.user = self.users[0]  # user1 из фикстуры
        
        self.user_data = {
            'username': 'user1',      # Из фикстуры
            'first_name': 'User',     # Из фикстуры  
            'last_name': 'One',       # Из фикстуры
            'email': '',              # В фикстуре нет email
            'password': 'testpass1'   # Пароль для тестов
        }

        # Данные для нового пользователя
        self.new_user_data = {
            'first_name': 'New',
            'last_name': 'User', 
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }

    def test_user_create_view_get(self):
        """Тест отображения формы регистрации (GET)"""
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')
        # Проверяем наличие формы вместо конкретного текста
        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_user_create_success(self):
        """Тест успешной регистрации пользователя (C - Create)"""
        response = self.client.post(reverse('user_create'), self.new_user_data)
        
        # Проверяем редирект на страницу входа
        self.assertRedirects(response, reverse('login'))
        
        # Проверяем что пользователь создан в базе
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_create_invalid_data(self):
        """Тест регистрации с невалидными данными"""
        invalid_data = self.new_user_data.copy()
        invalid_data['password2'] = 'differentpassword'
        
        response = self.client.post(reverse('user_create'), invalid_data)
        
        # Должен остаться на той же странице с ошибками
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create.html')
        
        # Проверяем что пользователь не создан
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_user_update_view_get_authenticated(self):
        """Тест отображения формы редактирования для авторизованного пользователя"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_update', args=[self.user.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/update.html')
        # Проверяем наличие формы и данных пользователя
        self.assertContains(response, '<form')
        self.assertContains(response, 'User')  # имя пользователя из фикстуры
        self.assertContains(response, 'user1')  # username из фикстуры

    def test_user_update_view_get_unauthenticated(self):
        """Тест доступа к форме редактирования без авторизации"""
        response = self.client.get(reverse('user_update', args=[self.user.id]))
        
        # Должен редиректить на страницу пользователей
        self.assertRedirects(response, reverse('users'))

    def test_user_update_success(self):
        """Тест успешного обновления пользователя (U - Update)"""
        self.client.force_login(self.user)
        
        updated_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        
        response = self.client.post(
            reverse('user_update', args=[self.user.id]),
            updated_data
        )
        
        # Проверяем редирект на список пользователей
        self.assertRedirects(response, reverse('users'))
        
        # Обновляем данные пользователя из базы
        self.user.refresh_from_db()
        
        # Проверяем что данные обновились
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_update_other_user(self):
        """Тест попытки редактирования чужого профиля"""
        other_user = self.users[1]  # user2 из фикстуры
        
        # Логинимся как первый пользователь
        self.client.force_login(self.user)
        
        # Пытаемся редактировать второго пользователя
        response = self.client.get(reverse('user_update', args=[other_user.id]))
        
        # Должен редиректить на список пользователей с ошибкой
        self.assertRedirects(response, reverse('users'))

    def test_user_delete_success(self):
        """Тест успешного удаления пользователя (D - Delete)"""
        self.client.force_login(self.user)
        
        user_id = self.user.id
        response = self.client.post(reverse('user_delete', args=[user_id]))
        
        # Проверяем редирект на список пользователей
        self.assertRedirects(response, reverse('users'))
        
        # Проверяем что пользователь удален из базы
        self.assertFalse(User.objects.filter(id=user_id).exists())

    def test_user_delete_other_user(self):
        """Тест попытки удаления чужого профиля"""
        other_user = self.users[1]  # user2 из фикстуры
        
        # Логинимся как первый пользователь
        self.client.force_login(self.user)
        
        # Пытаемся удалить второго пользователя
        response = self.client.get(reverse('user_delete', args=[other_user.id]))
        
        # Должен редиректить на список пользователей с ошибкой
        self.assertRedirects(response, reverse('users'))
        
        # Проверяем что второй пользователь не удален
        self.assertTrue(User.objects.filter(id=other_user.id).exists())