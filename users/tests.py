from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserCRUDTest(TestCase):
    def setUp(self):
        """Настройка тестовых данных"""
        self.client = Client()
        
        # Создаем тестового пользователя
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)
        
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
        self.assertContains(response, 'Test')  # имя пользователя
        self.assertContains(response, 'testuser')  # username

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
        # Создаем второго пользователя
        other_user = User.objects.create_user(
            username='otheruser',
            first_name='Other',
            last_name='User',
            email='other@example.com',
            password='otherpass123'
        )
        
        # Логинимся как первый пользователь
        self.client.force_login(self.user)
        
        # Пытаемся редактировать второго пользователя
        response = self.client.get(reverse('user_update', args=[other_user.id]))
        
        # Должен редиректить на список пользователей с ошибкой
        self.assertRedirects(response, reverse('users'))

    def test_user_delete_view_get_authenticated(self):
        """Тест отображения формы удаления для авторизованного пользователя (GET)"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('user_delete', args=[self.user.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')
        # Проверяем наличие формы и имени пользователя
        self.assertContains(response, '<form')
        self.assertContains(response, 'Test User')

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
        # Создаем второго пользователя
        other_user = User.objects.create_user(
            username='otheruser',
            first_name='Other',
            last_name='User',
            email='other@example.com',
            password='otherpass123'
        )
        
        # Логинимся как первый пользователь
        self.client.force_login(self.user)
        
        # Пытаемся удалить второго пользователя
        response = self.client.get(reverse('user_delete', args=[other_user.id]))
        
        # Должен редиректить на список пользователей с ошибкой
        self.assertRedirects(response, reverse('users'))
        
        # Проверяем что второй пользователь не удален
        self.assertTrue(User.objects.filter(id=other_user.id).exists())

    def test_user_list_view(self):
        """Тест отображения списка пользователей"""
        response = self.client.get(reverse('users'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/index.html')
        # Проверяем наличие таблицы и данных пользователя
        self.assertContains(response, '<table')
        self.assertContains(response, 'testuser')
        
        # Проверяем что пользователь есть в контексте
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 1)


class UserAuthenticationTest(TestCase):
    """Тесты аутентификации"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Тест отображения формы входа"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        # Проверяем наличие формы входа
        self.assertContains(response, '<form')
        self.assertContains(response, 'username')
        self.assertContains(response, 'password')
    
    def test_login_success(self):
        """Тест успешного входа"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertRedirects(response, reverse('home'))
    
    def test_login_failure(self):
        """Тест неудачного входа"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_logout(self):
        """Тест выхода из системы"""
        self.client.force_login(self.user)
        
        # Проверяем что пользователь авторизован
        self.assertTrue(self.user.is_authenticated)
        
        response = self.client.get(reverse('logout'))
        
        self.assertRedirects(response, reverse('home'))


class UserAccessTest(TestCase):
    """Тесты доступа к страницам"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_public_pages_access(self):
        """Тест доступа к публичным страницам без авторизации"""
        public_urls = [
            reverse('home'),
            reverse('users'),
            reverse('login'),
            reverse('user_create'),
        ]
        
        for url in public_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200,
                           f"Страница {url} должна быть доступна без авторизации")
    
    def test_protected_pages_redirect_when_anonymous(self):
        """Тест что защищенные страницы редиректят анонимных пользователей"""
        protected_urls = [
            reverse('user_update', args=[1]),
            reverse('user_delete', args=[1]),
            reverse('logout'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200,
                              f"Страница {url} не должна быть доступна без авторизации")


class UserFunctionalityTest(TestCase):
    """Тесты функциональности пользователей"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_full_name(self):
        """Тест метода get_full_name"""
        self.assertEqual(self.user.get_full_name(), 'Test User')
    
    def test_user_str_representation(self):
        """Тест строкового представления пользователя"""
        self.assertEqual(str(self.user), 'Test User')
    
    def test_user_creation_count(self):
        """Тест что пользователи создаются правильно"""
        initial_count = User.objects.count()
        
        # Создаем нового пользователя
        new_user = User.objects.create_user(
            username='newuser',
            first_name='New',
            last_name='User',
            email='new@example.com',
            password='newpass123'
        )
        
        self.assertEqual(User.objects.count(), initial_count + 1)
        self.assertEqual(new_user.get_full_name(), 'New User')