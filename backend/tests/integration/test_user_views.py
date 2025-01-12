from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class UserViewsTests(APITestCase):

    def setUp(self):
        # creat normal user
        self.user = User.objects.create_user(
            username='kr',
            email='kr@example.com',
            password='kr123',
        )
        # creat admin
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )

        self.client = APIClient()

    def test_register_user(self):
        """register a new user"""
        payload = dict(
            name="New User",
            email="newuser@example.com",
            password="newpassword123"
        )
        response = self.client.post('/api/users/register/', payload)
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert data["name"] == payload["name"]
        # self.assertEqual(response.data['username'], 'newuser@example.com')

    def test_login_user(self):
        payload = {
            'username': self.user.username,
            'password': 'kr123'
        }
        response = self.client.post('/api/users/login/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['isAdmin'], False)

    def test_get_users_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # test the regular user
        regular_user = response.data[0]
        print(regular_user)
        self.assertEqual(regular_user['username'],self.user.username)
        self.assertEqual(regular_user['email'], self.user.email)
        self.assertEqual(regular_user['name'], self.user.username)
        self.assertEqual(regular_user['isAdmin'], False)
        # test the admin user
        admin_user = response.data[1]
        print(admin_user)
        self.assertEqual(admin_user['username'], self.admin_user.username)
        self.assertEqual(admin_user['email'], self.admin_user.email)
        self.assertEqual(admin_user['name'], self.admin_user.username)
        self.assertEqual(admin_user['isAdmin'], True)
        
        # Check data order
        self.assertTrue(response.data[0]['id'] < response.data[1]['id'])

    def test_get_users_as_non_admin(self):
        "Test preventing a regular user from retrieving all users"      
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_profile(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'TR',
            'email': 'TR@example.com',
            'password': 'TR123'
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put('/api/users/profile/update/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(response.data['username'], payload['email'])
        self.assertEqual(response.data['email'], payload['email'])
        self.assertEqual(response.data['name'], payload['name'])
        self.assertTrue(self.user.check_password('TR123'))
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['isAdmin'], False)
        
    def test_delete_user_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/users/delete/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/users/delete/{self.admin_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_by_id_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['username'], self.user.username)

    def test_get_user_by_id_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_register_user_with_existing_username(self):
        data = {
            'name': 'Duplicate User',
            'email': 'kr@example.com', 
            'password': 'newpassword123'
        }
        response = self.client.post('/api/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
         

    def test_register_user_with_missing_fields(self):
        """register a new user"""
        payload = dict(
            name="New User2",
            email="uesr2@example.com",
            # no password 
        )
        response = self.client.post('/api/users/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.data)
        self.assertEqual(response.data['detail'], 'User with this email is already registered')
        # assert response.data["name"] == payload["name"]
        # self.assertIn("name", response.data) 

    def test_register_user_with_existing_email(self):
        """Test registering a user with an already registered email"""
        email = self.user.email
        if not User.objects.filter(email=email).exists():
            User.objects.create_user(
                username='existinguser',
                email=email,
                password='password123'
            )
        payload = {
            'email': email,
            'password': 'newpassword123'
        }
        response = self.client.post('/api/users/register/', payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.data)
        self.assertEqual(response.data['detail'], 'User with this email is already registered')
       
    def test_get_user_profile_with_invalid_token(self):
        self.client.force_authenticate(user=None) 
        response = self.client.get('/api/users/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  

    def test_get_users_after_registering_new_user(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'name': 'New Registered User',
            'email': 'newuser2@example.com',
            'password': 'newpassword123'
        }
        self.client.post('/api/users/register/', data)  
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  

    def test_login_user_with_wrong_password(self):
        """Test login with a wrong password"""
        payload = {
            'username': self.user.username,
            'password': 'wrongpassword123'  # Incorrect password
        }
        response = self.client.post('/api/users/login/', payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)






