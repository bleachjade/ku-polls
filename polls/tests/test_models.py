import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    """Test question condition in model class."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """is_published() return False if current date is before question's publication date."""
        time = timezone.now() + datetime.timedelta(days=10)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_old_question(self):
        """is_published() return Ture if current date is after question's publication date."""
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_present_question(self):
        """is_published() return Ture if current date is on question's publication date."""
        time = timezone.now()
        present_question = Question(pub_date=time)
        self.assertIs(present_question.is_published(), True)

    # can_vote condition:
    # pub_date < now < end_date == True
    # pub_date = now(< end_date) == True
    # pub_date > now == False
    # now > end_date == False
    # now = end_date == False
    def test_can_vote_with_now_is_after_pub_date_and_before_end_date(self):
        """can_vote() return True if you're voting currently is between pub_date and end_date."""
        pub_date = timezone.now() - datetime.timedelta(days=2)
        end_date = timezone.now() + datetime.timedelta(days=10)
        now = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(now.can_vote(), True)

    def test_can_vote_with_now_equal_to_pub_date(self):
        """can_vote() return True if you're voting currently is on pub_date."""
        pub_date = timezone.now()
        end_date = timezone.now() + datetime.timedelta(days=1)
        now = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(now.can_vote(), True)

    def test_can_vote_with_now_is_before_pub_date(self):
        """can_vote() return False if you're voting currently is before pub_date."""
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = timezone.now()
        before = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(before.can_vote(), False)

    def test_can_vote_with_now_is_after_end_date(self):
        """can_vote() return False if you're voting currently is after end_date."""
        pub_date = timezone.now()
        end_date = timezone.now() - datetime.timedelta(days=1)
        before = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(before.can_vote(), False)

    def test_can_vote_with_now_is_equal_to_end_date(self):
        """can_vote() return False if you're voting currently is on end_date."""
        pub_date = timezone.now() + datetime.timedelta(days=1)
        end_date = timezone.now()
        before = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(before.can_vote(), False)