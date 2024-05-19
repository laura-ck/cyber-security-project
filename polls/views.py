from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.http import HttpResponseForbidden

from .models import Choice, Question
from django.db.models import Q

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def search(request):
    query = request.GET.get('query', '')
    raw_query = f"SELECT * FROM polls_question WHERE question_text LIKE '%{query}%'"
    questions = Question.objects.raw(raw_query)
    return render(request, 'polls/search_results.html', {'questions': questions})

# Fix: Use parameterized queries to prevent SQL injection
#def search(request):
#    query = request.GET.get('query', '').strip()

#    if not query or len(query) < 2 or '%' in query:
#        error_message = "Invalid search query. Please enter at least 2 characters and avoid special characters."
#        return render(request, 'polls/search_results.html', {'questions': [], 'error_message': error_message})
#    
#    questions = Question.objects.filter(Q(question_text__icontains=query))

#    return render(request, 'polls/search_results.html', {'questions': questions})

def admin_profile(request, user_id):
    admin_user = get_object_or_404(User, id=user_id, is_superuser=True)
    log_entries = LogEntry.objects.filter(user_id=user_id)
    return render(request, 'polls/admin_profile.html', {'admin_user': admin_user, 'log_entries': log_entries})

#def admin_profile(request, user_id):
#    if not request.user.is_superuser and request.user.id != user_id:
#        return HttpResponseForbidden("You are not allowed to view this profile.")
#    admin_user = get_object_or_404(User, id=user_id, is_superuser=True)
#    log_entries = LogEntry.objects.filter(user_id=user_id)
#    return render(request, 'admin_profile.html', {'admin_user': admin_user, 'log_entries': log_entries})