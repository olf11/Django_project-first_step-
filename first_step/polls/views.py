from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from rest_framework import viewsets, permissions, generics
from .models import Choice, Question, UserVote
from .serializers import QuestionSerializer, ChoiceSerializer
from rest_framework.reverse import reverse
from .permisions import IsOwnerOrReadOnly


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):

        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        user = UserVote()
        user.ip = user.get_user_ip(self.request)
        user.question = Question.objects.get(pk=self.kwargs['pk'])
        context['voted_already'] = user.vote_already()
        return context

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = UserVote()
    user.ip = user.get_user_ip(request)
    user.question = question
    if user.vote_already():
        return HttpResponse('You voted')
    if request.POST.get('choice'):
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            user.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
