"""
URL configuration for aptitude_prep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import  TokenRefreshView
from aptitude.views import MyTokenObtainPairView, login_view, signup_view, home_view, logout_view, subtopics_view, video_lesson_view, practice_view, practice_new_view, boss_dashboard, subtopic_phase_view, question_phase_view, analytics_view, contests_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('aptitude.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Web interface URLs
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout_view'),
    path('home/', home_view, name='home'),
    path('signup/', signup_view, name='signup'),
    path('analytics/', analytics_view, name='analytics'),
    path('contests/', contests_view, name='contests'),
    path("topics/<int:topic_id>/", subtopics_view, name="subtopics"),
    path("subtopics/<int:subtopic_id>/", video_lesson_view, name="video_lesson"),
    path("practice/<int:subtopic_id>/<str:difficulty>/<int:q_index>/", practice_view, name="practice"),
    path("practice-new/<int:subtopic_id>/<str:difficulty>/<int:q_index>/", practice_new_view, name="practice_new"),
    path("boss/dashboard/", boss_dashboard, name="boss_dashboard"),
    path("boss/subtopics/<int:topic_id>/", subtopic_phase_view, name="subtopic_phase"),
    path("boss/questions/<int:subtopic_id>/", question_phase_view, name="question_phase"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)