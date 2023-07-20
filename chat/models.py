from django.db import models

# Create your models here.
import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Character(models.Model):
    name=models.CharField(max_length=100)
    system=models.TextField()


class Message(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_from_me"
    )
    to_character = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_to_me"
    )
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.from_user.name} to {self.to_character.username}: {self.content} [{self.timestamp}]"