from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    capabilities = models.JSONField()
    endpoint_url = models.URLField()
    status = models.CharField(default='active', max_length=20)

    def __str__(self):
        return self.name