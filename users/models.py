from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class AboutQuestion(models.Model):
    institution_name = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    course_number = models.CharField(max_length=30)
    marks = models.IntegerField()
    time = models.CharField(max_length=8)
    total_questions = models.IntegerField(default=6)
    to_be_answerd = models.IntegerField(default=4)

    def __str__(self):
        return'{self.institution_name}'.format(self=self)

