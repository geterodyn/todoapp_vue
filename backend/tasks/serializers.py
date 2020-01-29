from tasks.models import Todo
from rest_framework import serializers

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'description', 'is_completed', 'priority']