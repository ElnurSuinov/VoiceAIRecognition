from django.db import models

# Create your models here.
class DialogueLog(models.Model):
    user_text = models.TextField()
    intent = models.CharField(max_length=50)
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} | {self.intent}"