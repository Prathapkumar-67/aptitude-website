from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubtopicViewSet)
router.register(r'lessons', VideoLessonViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)
router.register(r'streaks', UserStreakViewSet, basename='streak')
router.register(r'notifications', NotificationSettingViewSet, basename='notification')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),  # API routes
    path('me/', MeView.as_view(), name='me'),
]
