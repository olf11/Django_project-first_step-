from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    id = id(question_text)
    user = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE)

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published_recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    id = id(choice_text)
    user = models.ForeignKey('auth.User', related_name='choice', on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text


class UserVote(models.Model):
    ip = models.GenericIPAddressField(verbose_name='user_ip')
    question = models.ForeignKey(Question, verbose_name='user questions votes', on_delete=models.CASCADE)

    def __str__(self):
        return self.ip

    def get_user_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def vote_already(self):
        user_list = UserVote.objects.filter(ip=self.ip, question=self.question)
        return len(user_list) > 0
