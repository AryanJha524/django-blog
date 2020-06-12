from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    # pass in user db and deletes post if user deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  # formatting for printing post objects
        return self.title

    # returns string of url to the specific post to be handled by the view for creating post
    # (returns to detaild view of post created)
    '''def get_absolute_url(self):
                    return reverse('post-detail', kwargs={'pk': self.pk})'''
