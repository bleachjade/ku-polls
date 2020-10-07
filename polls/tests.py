import datetime

from django.http import HttpResponseRedirect
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from .models import Question

def create_question(question_text, days):
    """Create a question for polls app.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTest(TestCase):
    """Test question index page."""

    def setUp(self):
        """Set up a client to request later."""
        self.client = Client()

    def test_no_question(self):
        """If no question exist, an approprite message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    """Test question detail page."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 not found."""
        future_question = create_question(question_text='Future question.', days=5)
        url = HttpResponseRedirect(reverse('polls:detail', args=(future_question.id,)))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


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

