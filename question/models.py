from django.db import models
from django.urls import reverse

class Questions(models.Model):
    author = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    marks = models.IntegerField(default=range(1,10))
    PUBLIC = 'PUBLIC'
    POTECTED = 'POTECTED'
    PRIVATE = 'PRIVATE'
    ACCESS_MODIFIER_CHOICES = (
        (PUBLIC, 'PUBLIC'),
        (POTECTED, 'POTECTED'),
        (PRIVATE, 'PRIVATE'),
    )
    access_modifier = models.CharField(max_length=8, choices=ACCESS_MODIFIER_CHOICES, default=PUBLIC)
    question_text = models.TextField(default='Please describes your question..')
    is_covered = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('question:detail' , kwargs={'pk':self.pk})  #{% url 'myapp:my_url_name' %}

    def __str__(self):
        return '{self.author}'.format(self=self) + ' - ' + '{self.subject}'.format(self=self)



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

