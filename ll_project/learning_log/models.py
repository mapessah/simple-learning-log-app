from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    text = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    
    # string representation of a topic
    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        else:
            return self.text

class Entry(models.Model):
    # The entries model
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
    
    # The string representation of an entry
    def __str__(self):
        if len(self.text) > 50:
            return f'{self.text[:50]}...'
        else:
            return self.text
