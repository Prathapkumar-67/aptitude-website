from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use custom authentication backend that handles email
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            if user.role == 'boss':
                return redirect('boss_dashboard')
            else:
                return redirect('home')
        else:
            return render(request, 'aptitude/login.html', {'error': 'Invalid credentials'})

    return render(request, 'aptitude/login.html')


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        errors = {}

        if User.objects.filter(username=username).exists():
            errors["username"] = "Username already taken."
        if User.objects.filter(email=email).exists():
            errors["email"] = "Email already registered."

        if errors:
            return render(request, "aptitude/signup.html", {"errors": errors})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='student'
        )

        login(request, user)  # Automatically log in the new user
        return redirect("home")

    return render(request, "aptitude/signup.html")



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    # Organize topics by category, excluding specified topics
    excluded_topics = ['Number Theory', 'Data Science', 'Intensive Data Analysis']

    common_topics = Topic.objects.filter(category='Common').exclude(name__in=excluded_topics).order_by("display_order")
    it_topics = Topic.objects.filter(category='IT-specific').exclude(name__in=excluded_topics).order_by("display_order")
    govt_topics = Topic.objects.filter(category='Govt-specific').exclude(name__in=excluded_topics).order_by("display_order")

    context = {
        'common_topics': common_topics,
        'it_topics': it_topics,
        'govt_topics': govt_topics,
    }
    return render(request, "aptitude/home.html", context)


@login_required
def analytics_view(request):
    """Analytics page showing user's progress and statistics"""
    # Get user's visited topics and questions completed
    # For now, we'll show placeholder data
    context = {
        'topics_visited': 5,
        'questions_completed': 25,
        'average_score': 78,
        'time_spent': '2h 30m',
    }
    return render(request, "aptitude/analytics.html", context)


@login_required
def contests_view(request):
    """Contests page - currently showing coming soon"""
    return render(request, "aptitude/contests.html")


@login_required
def subtopics_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    subtopics = Subtopic.objects.filter(topic=topic).order_by('display_order')
    return render(request, "aptitude/subtopics.html", {
        "topic": topic,
        "subtopics": subtopics
    })

@login_required
def video_lesson_view(request, subtopic_id):
    subtopic = get_object_or_404(Subtopic, id=subtopic_id)
    video = VideoLesson.objects.filter(subtopic=subtopic).first()
    notes = Note.objects.filter(subtopic=subtopic)
    resources = Resource.objects.filter(subtopic=subtopic)
    
    return render(request, "aptitude/video_lesson.html", {
        "subtopic": subtopic,
        "video": video,
        "notes": notes,
        "resources": resources,
    })


@login_required
def practice_view(request, subtopic_id, difficulty, q_index=0):
    subtopic = get_object_or_404(Subtopic, id=subtopic_id)
    questions = Question.objects.filter(subtopic=subtopic, difficulty=difficulty).order_by('id')

    if not questions.exists():
        return render(request, "aptitude/no_questions.html", {
            "subtopic": subtopic,
            "difficulty": difficulty,
            "message": "No questions yet for this difficulty level."
        })

    try:
        question = questions[q_index]
    except IndexError:
        return render(request, "aptitude/practice_complete.html", {
            "subtopic": subtopic,
            "difficulty": difficulty,
            "message": "You've completed all questions!"
        })

    options = Option.objects.filter(question=question)

    if request.method == "POST":
        selected_option_id = int(request.POST.get("option_id"))
        selected_option = get_object_or_404(Option, id=selected_option_id)

        is_correct = selected_option.is_correct
        UserAnswer.objects.create(
            user=request.user,
            question=question,
            option=selected_option,
            is_correct=is_correct,
            time_taken=int(request.POST.get("time_taken", 0))
        )

        # Redirect to next question
        return redirect('practice', subtopic_id=subtopic.id, difficulty=difficulty, q_index=q_index+1)

    return render(request, "aptitude/practice.html", {
        "subtopic": subtopic,
        "question": question,
        "options": options,
        "difficulty": difficulty,
        "q_index": q_index,
    })


@login_required
def practice_new_view(request, subtopic_id, difficulty, q_index=0):
    subtopic = get_object_or_404(Subtopic, id=subtopic_id)
    questions = Question.objects.filter(subtopic=subtopic, difficulty=difficulty).order_by('id')

    if not questions.exists():
        return render(request, "aptitude/no_questions.html", {
            "subtopic": subtopic,
            "difficulty": difficulty,
            "message": "No questions yet for this difficulty level."
        })

    try:
        question = questions[q_index]
    except IndexError:
        return render(request, "aptitude/practice_complete.html", {
            "subtopic": subtopic,
            "difficulty": difficulty,
            "message": "You've completed all questions!"
        })

    options = Option.objects.filter(question=question)

    # Calculate progress
    total_questions = questions.count()
    user_answers = UserAnswer.objects.filter(user=request.user, question__in=questions)
    solved_count = user_answers.count()
    remaining_count = total_questions - solved_count

    if request.method == "POST":
        selected_option_id = int(request.POST.get("option_id"))
        selected_option = get_object_or_404(Option, id=selected_option_id)

        is_correct = selected_option.is_correct
        UserAnswer.objects.create(
            user=request.user,
            question=question,
            option=selected_option,
            is_correct=is_correct,
            time_taken=int(request.POST.get("time_taken", 0))
        )

        # Redirect to next question
        return redirect('practice_new', subtopic_id=subtopic.id, difficulty=difficulty, q_index=q_index+1)

    return render(request, "aptitude/practice_new.html", {
        "subtopic": subtopic,
        "question": question,
        "options": options,
        "difficulty": difficulty,
        "q_index": q_index,
        "total_questions": total_questions,
        "solved_count": solved_count,
        "remaining_count": remaining_count,
    })
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def boss_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'boss':
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper

from .models import Topic, Subtopic
#from .decorators import boss_required  # or use local function

@boss_required
def boss_dashboard(request):
    from .models import Question, User
    topics = Topic.objects.all().order_by("display_order")

    # Calculate statistics
    total_subtopics = Subtopic.objects.count()
    total_questions = Question.objects.count()
    total_users = User.objects.filter(role='student').count()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_topic":
            name = request.POST.get("name")
            category = request.POST.get("category")

            # Find the next display_order
            max_order = Topic.objects.aggregate(max_order=models.Max('display_order'))['max_order'] or 0
            display_order = max_order + 1

            Topic.objects.create(
                name=name,
                category=category,
                display_order=display_order,
                created_by=request.user
            )
        
        elif action == "edit_topic":
            topic_id = request.POST.get("topic_id")
            name = request.POST.get("name")
            category = request.POST.get("category")

            topic = Topic.objects.get(id=topic_id)
            topic.name = name
            topic.category = category
            topic.save()

        elif action == "delete_topic":
            topic_id = request.POST.get("topic_id")
            topic = Topic.objects.get(id=topic_id)
            if Subtopic.objects.filter(topic=topic).exists():
                return render(request, "aptitude/boss_dashboard.html", {
                    "topics": topics,
                    "total_subtopics": total_subtopics,
                    "total_questions": total_questions,
                    "total_users": total_users,
                    "error": "Cannot delete topic. Subtopics exist."
                })
            topic.delete()

        return redirect("boss_dashboard")  # Optional: to prevent form resubmission on refresh

    return render(request, "aptitude/boss_dashboard.html", {
        "topics": topics,
        "total_subtopics": total_subtopics,
        "total_questions": total_questions,
        "total_users": total_users,
    })


@boss_required
def subtopic_phase_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    subtopics = Subtopic.objects.filter(topic=topic).order_by('display_order')

    # Count questions by difficulty for each subtopic
    subtopic_data = []
    for subtopic in subtopics:
        easy_count = Question.objects.filter(subtopic=subtopic, difficulty='easy').count()
        medium_count = Question.objects.filter(subtopic=subtopic, difficulty='medium').count()
        hard_count = Question.objects.filter(subtopic=subtopic, difficulty='hard').count()

        subtopic_data.append({
            'subtopic': subtopic,
            'easy_count': easy_count,
            'medium_count': medium_count,
            'hard_count': hard_count,
            'total_count': easy_count + medium_count + hard_count
        })

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_subtopic":
            name = request.POST.get("name")

            # Find the next display_order
            max_order = Subtopic.objects.filter(topic=topic).aggregate(max_order=models.Max('display_order'))['max_order'] or 0
            display_order = max_order + 1

            Subtopic.objects.create(
                name=name,
                topic=topic,
                display_order=display_order,
                created_by=request.user
            )

        elif action == "edit_subtopic":
            subtopic_id = request.POST.get("subtopic_id")
            name = request.POST.get("name")

            subtopic = get_object_or_404(Subtopic, id=subtopic_id)
            subtopic.name = name
            subtopic.save()

        elif action == "delete_subtopic":
            subtopic_id = request.POST.get("subtopic_id")
            subtopic = get_object_or_404(Subtopic, id=subtopic_id)
            if Question.objects.filter(subtopic=subtopic).exists():
                return render(request, "aptitude/subtopic_phase.html", {
                    "topic": topic,
                    "subtopic_data": subtopic_data,
                    "error": "Cannot delete subtopic. Questions exist."
                })
            subtopic.delete()

        return redirect("subtopic_phase", topic_id=topic.id)

    return render(request, "aptitude/subtopic_phase.html", {
        "topic": topic,
        "subtopic_data": subtopic_data
    })


@boss_required
def question_phase_view(request, subtopic_id):
    subtopic = get_object_or_404(Subtopic, id=subtopic_id)

    # Get filter parameter
    difficulty_filter = request.GET.get('difficulty', 'all')

    # Filter questions based on difficulty
    if difficulty_filter == 'all':
        questions = Question.objects.filter(subtopic=subtopic).order_by('id')
    else:
        questions = Question.objects.filter(subtopic=subtopic, difficulty=difficulty_filter).order_by('id')

    # Get questions with their options
    question_data = []
    for question in questions:
        options = Option.objects.filter(question=question)
        question_data.append({
            'question': question,
            'options': options
        })

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_question":
            text = request.POST.get("text")
            difficulty = request.POST.get("difficulty")
            time_limit = request.POST.get("time_limit", 60)

            option1 = request.POST.get("option1")
            option2 = request.POST.get("option2")
            option3 = request.POST.get("option3")
            option4 = request.POST.get("option4")
            correct_option = request.POST.get("correct_option")

            # Create question
            question = Question.objects.create(
                subtopic=subtopic,
                text=text,
                difficulty=difficulty,
                time_limit=int(time_limit),
                created_by=request.user
            )

            # Create options
            options_data = [
                (option1, correct_option == "1"),
                (option2, correct_option == "2"),
                (option3, correct_option == "3"),
                (option4, correct_option == "4")
            ]

            for option_text, is_correct in options_data:
                Option.objects.create(
                    question=question,
                    text=option_text,
                    is_correct=is_correct
                )

        elif action == "edit_question":
            question_id = request.POST.get("question_id")
            text = request.POST.get("text")
            difficulty = request.POST.get("difficulty")
            time_limit = request.POST.get("time_limit", 60)

            option1 = request.POST.get("option1")
            option2 = request.POST.get("option2")
            option3 = request.POST.get("option3")
            option4 = request.POST.get("option4")
            correct_option = request.POST.get("correct_option")

            # Update question
            question = get_object_or_404(Question, id=question_id)
            question.text = text
            question.difficulty = difficulty
            question.time_limit = int(time_limit)
            question.save()

            # Delete existing options and create new ones
            Option.objects.filter(question=question).delete()

            options_data = [
                (option1, correct_option == "1"),
                (option2, correct_option == "2"),
                (option3, correct_option == "3"),
                (option4, correct_option == "4")
            ]

            for option_text, is_correct in options_data:
                Option.objects.create(
                    question=question,
                    text=option_text,
                    is_correct=is_correct
                )

        elif action == "delete_question":
            question_id = request.POST.get("question_id")
            question = get_object_or_404(Question, id=question_id)
            question.delete()  # This will also delete related options due to CASCADE

        return redirect(f"{request.path}?difficulty={difficulty_filter}")

    return render(request, "aptitude/question_phase.html", {
        "subtopic": subtopic,
        "question_data": question_data,
        "difficulty_filter": difficulty_filter
    })



from rest_framework import viewsets,generics
from .models import *
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []  # Public access

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer

class VideoLessonViewSet(viewsets.ModelViewSet):
    queryset = VideoLesson.objects.all()
    serializer_class = VideoLessonSerializer

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "role": user.role
        })

class UserStreakViewSet(viewsets.ModelViewSet):
    serializer_class = UserStreakSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserStreak.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NotificationSettingViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSettingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationSetting.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)