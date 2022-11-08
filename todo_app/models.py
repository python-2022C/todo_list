from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Task(models.Model):
    '''Schema for Task table'''

    title        = models.CharField(max_length=64)
    description  = models.CharField(max_length=255, blank=True, default="")
    is_completed = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    deatline     = models.DateTimeField()
    importance   = models.SmallIntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)


    def to_json(self) -> dict:
        '''to convert a task object to a dict.
        
        Args:
            self (object): task object.

        Returns:
            dict: task as dict.
        '''

        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_completed': self.is_completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deatline': self.deatline,
            'importance': self.importance,
            'customer': User.objects.get(username=self.customer).username
        }


    def __str__(self) -> str:
        return super().__str__(self.title)
