import datetime

from django.db import models
from django.utils import timezone
import hashlib


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    #Cryptographic failure (weak encryption algorithm):
    def encrypt(self, text):
        return hashlib.md5(text.encode()).hexdigest()
    
    #How to fix this flaw:
    #Use a SECURE hash algorithm, for example:
    #def encrypt(self, text)
        #return hashlib.sha256(text.encode()).hexdigest()

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
