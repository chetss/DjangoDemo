from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Post (models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    # timezone.now() is a function
    # we don't want to execute the fuction we just want to pass the
    # fuction value as default that's why we don't use ()
    data_posted = models.DateTimeField(default=timezone.now)

    # on_delete = models.CASCADE > when the user is deleted then delete the post which are
    # created by him

    # USER >  To access the specfic user we have to access the User table created
    #  by the django

    #  ForeignKey()  > it is used because a user can add muliple post
    #  but the post will only belong to the specfic user
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post-detail', kwargs={'pk': self.pk})
