from django.db import models

# Create your models here.
class Todo(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Высокий приоритет'),
        (2, 'Средний приоритет'),
        (3, 'Низкий приоритет'),
    ]

    description = models.CharField(max_length=256)
    is_completed = models.BooleanField('выполнено', default=False)
    priority = models.IntegerField('приоритет', choices=PRIORITY_CHOICES, default=2)

    def to_dict(self):
        return {
            'uid': self.id,
            'description': self.description,
            'priority': self.priority,
            'is_completed': self.is_completed
        }

    def __str__(self):
        return self.description.lower()

    class Meta:
        ordering = ('id',)

