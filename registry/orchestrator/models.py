from django.db import models

class Task(models.Model):
    task_id = models.CharField(max_length=100)
    capability = models.CharField(max_length=50)
    input_text = models.TextField()
    result = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)