import datetime
from datetime import date, timedelta

from django import forms
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # end_date = models.DateTimeField(widget=forms.DateTimeInput('%m/%d/%y %H:%M'))
    end_date = models.DateTimeField('ending date', default=timezone.now())

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    # def valid_end_date(self):
    #     if self.end_date < self.pub_date:
    #         raise forms.ValidationError("End date should be greater than publish date.")

    def is_published(self):
        return timezone.now() >= self.pub_date

    def can_vote(self):
        return self.end_date > timezone.now() >= self.pub_date

    

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    