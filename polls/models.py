import datetime
from typing import cast

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Create a question model to use in a polls app."""

    question_text = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    # set end_date default to 10 days
    end_date = models.DateTimeField('ending date', default=timezone.now() + datetime.timedelta(days=10))
    voters = models.ManyToManyField(User, through="Vote")

    def __str__(self):
        """Return str of the question text."""
        return self.question_text

    def was_published_recently(self):
        """Check whether this question was published recently or not."""
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    # def valid_end_date(self):
    #     if self.end_date < self.pub_date:
    #         raise forms.ValidationError("End date should be greater than publish date.")

    def is_published(self):
        """Check whether this question is published or not."""
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """Check whether user can vote or not."""
        return self.end_date > timezone.now() >= self.pub_date

    
    # @property
    # def choices(self):
    #     return self.choice_set.all()

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Create a choice model to use in a polls app."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    

    def __str__(self):
        """Return str of choice text."""
        return self.choice_text

class Vote(models.Model):
    """Create a model to track user vote."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, 
                  on_delete=models.CASCADE)


    