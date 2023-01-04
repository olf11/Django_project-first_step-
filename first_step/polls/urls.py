from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'question', views.QuestionViewSet, basename='question')
router.register(r'choice', views.ChoiceViewSet, basename='choice')
# 21.12.22
# router.register(r'user', views.UserViewSet, basename='user')


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # path('question/', views.QuestionList.as_view(), name='question_swag'),
    # path('choice/', views.ChoiceList.as_view(), name='choice_swag'),
    path('', include(router.urls)),

]