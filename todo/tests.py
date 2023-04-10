from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from todo.models import Todo
from todo.serializers import TodoSerializer

# Create your tests here.
class TodoViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.todo = Todo.objects.create(user=self.user, title='Test todo')

    def test_list_todos(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('todo-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_todo(self):
        data = {'title': 'New todo', 'user': self.user.id}
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('todo-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New todo')
        self.assertEqual(response.data['user'], self.user.id)

    def test_update_todo(self):
        data = {'title': 'Updated todo'}
        self.client.login(username='testuser', password='testpass')
        response = self.client.patch(reverse('todo-detail', args=[self.todo.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated todo')

    def test_delete_todo(self):
        self.client.login(username='testuser', password='testpass')
        todo = Todo.objects.create(user=self.user, title='Delete me')
        response = self.client.delete(reverse('todo-detail', args=[todo.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.filter(id=todo.id).exists(), False)

    def test_reorder_todos(self):
        self.client.login(username='testuser', password='testpass')
        todo1 = Todo.objects.create(user=self.user, title='Todo 1', order=1)
        todo2 = Todo.objects.create(user=self.user, title='Todo 2', order=2)
        todo3 = Todo.objects.create(user=self.user, title='Todo 3', order=3)
        todo_ids = [todo3.id, todo1.id, todo2.id]
        data = {'todo_ids': todo_ids}
        response = self.client.post(reverse('todo-reorder'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.get(id=todo1.id).order, 2)
        self.assertEqual(Todo.objects.get(id=todo2.id).order, 3)
        self.assertEqual(Todo.objects.get(id=todo3.id).order, 1)

    def test_update_todo_title(self):
        todo = Todo.objects.create(user=self.user, title='Todo')
        self.client.login(username='testuser', password='testpass')
        data = {'title': 'Updated todo'}
        response = self.client.patch(reverse('todo-detail', args=[todo.id]), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Updated todo", [todo.title for todo in Todo.objects.all()])

    def test_reorder_todos(self):
        self.client.login(username='testuser', password='testpass')
        todo1 = Todo.objects.create(user=self.user, title='Todo 1')
        todo2 = Todo.objects.create(user=self.user, title='Todo 2')
        todo3 = Todo.objects.create(user=self.user, title='Todo 3')
        todo_titles = ['Todo 3', 'Todo 1', 'Todo 2']
        todo_ids = [todo3.id, todo1.id, todo2.id]
        data = {'todo_ids': todo_ids}
        response = self.client.post(reverse('todo-reorder'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual([todo.title for todo in Todo.objects.all()], todo_titles)

