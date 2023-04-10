from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer, TodoCreateSerializer, TodoUpdateSerializer

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('order')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return TodoCreateSerializer
        elif self.action == 'update':
            return TodoUpdateSerializer
        else:
            return TodoSerializer

    @action(methods=['POST'], detail=False)
    def reorder(self, request):
        todo_ids = request.data.get('todo_ids', [])
        order = 1
        for todo_id in todo_ids:
            todo = Todo.objects.get(id=todo_id, user=request.user)
            todo.order = order
            todo.save()
            order += 1
        todos = Todo.objects.filter(id__in=todo_ids).order_by('order')
        for i, todo in enumerate(todos, start=1):
            todo.order = i
            todo.save()
        return Response({'message': 'Todos reordered successfully'})

    def delete(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo.user != request.user:
            return Response({'message': 'You can only delete your own todos'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)