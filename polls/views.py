from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F

from .models import Question, Choice, Vote


class IndexView(generic.ListView):
    """Show index view whic is a list of all polls question."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including those set to be published in the future)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

    # def show_valid_question(self):
    #     return Question.objects.filter(
    #         end_date__mt=timezone.now()
    #     )


class DetailView(generic.DetailView):
    """Show detail view which is a list of question's choice."""

    model = Question
    template_name = 'polls/detail.html'
    # messages.add_message(request, messages.ERROR,  'An unexpected error occured.')

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    # def redirect_uesr_to_index(request, pk, self):
    #     question = get_object_or_404(Question, pk=pk)
    #     if not question.can_vote():
    #         messages.error(request, 'Voting is not allowed!')
    #         return redirect('polls:index')
    #     return render(request, 'polls/detail.html', {'question': question})


# def test_vote_detail(request):
#     detail = DetailView()
#     context = dict(detail)
#     messages.error(request, 'An error occurs')

class ResultsView(generic.DetailView):
    """Show a result page(a page with a list of all choice in that polls question)."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Vote function for polls app."""
    question = get_object_or_404(Question, pk=question_id)
    # user can vote once per poll.
    if Vote.objects.filter(question_id=question_id, user_id=request.user.id).exists():
        return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "You've already vote for this poll."
        })
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # print(Vote.objects.filter(question_id=question_id, user_id=request.user.id).exists())
        # if request.user == Vote.authen_vote(request):
        #     messages.error(request, "you've already vote for this poll")
        #     # return redirect('polls:index')

        # else:
        selected_choice.votes +=1
        selected_choice.save()
        v = Vote(user=request.user, question=question)
        v.save()
    
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def valid_vote(request, pk):
    """Check if the polls is valid to vote or not."""
    question = get_object_or_404(Question, pk=pk)
    if not question.can_vote():
        messages.error(request, f'You are not allowed to vote in the "{question.question_text}" poll!')
        return redirect('polls:index')
    return render(request, 'polls/detail.html', {'question': question})

def show_vote(request, pk):
    question = get_object_or_404(Question, pk=pk)
    choice = get_object_or_404(Choice, pk=pk)
    if not Vote.objects.filter(question_id=pk, user_id=request.user.id).exists():
        return redirect('polls:detail')
    return render(request, 'polls/results.html', {'questiion': question, 'choice': choice})

