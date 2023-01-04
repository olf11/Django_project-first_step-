from rest_framework import serializers, permissions
from rest_framework.permissions import IsAuthenticated

from .models import Question, Choice
from django.contrib.auth.models import User


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'id', 'user']


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['question', 'choice_text', 'votes', 'id']

