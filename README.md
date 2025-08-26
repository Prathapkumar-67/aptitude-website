# 🎯 Aptitude Prep - Comprehensive Learning Platform

A full-stack web application designed for aptitude test preparation, featuring a Django REST API backend and a Next.js frontend. The platform provides structured learning paths, practice questions, analytics, and progress tracking for students preparing for various competitive exams.

## 🌟 Features

### 📚 Learning Management
- **Categorized Topics**: Organized into Common, IT-specific, and Government-specific categories
- **Structured Learning Path**: Topics → Subtopics → Video Lessons → Practice Questions
- **Difficulty Levels**: Easy, Medium, and Hard questions for progressive learning
- **Video Lessons**: Integrated video content for each subtopic
- **Study Resources**: Notes and additional learning materials

### 🎮 Interactive Practice
- **Question Practice**: Multiple-choice questions with instant feedback
- **Time Tracking**: Monitor time spent on each question
- **Progress Tracking**: Track completion status and performance
- **Streak System**: Daily learning streaks to maintain consistency
- **Two Practice Modes**: Standard and enhanced practice interfaces

### 📊 Analytics & Progress
- **Personal Analytics**: Track topics visited, questions completed, and average scores
- **Performance Metrics**: Detailed statistics on learning progress
- **Time Management**: Monitor time spent studying
- **Achievement Tracking**: Visual progress indicators

### 👥 User Management
- **Role-based Access**: Student and Boss (Admin) roles
- **Email Authentication**: Secure login using email addresses
- **User Profiles**: Personalized learning experiences
- **Session Management**: JWT-based authentication

### 🏆 Additional Features
- **Contests**: Competitive learning environment (Coming Soon)
- **Notifications**: Customizable notification settings
- **Responsive Design**: Works seamlessly across devices
- **Admin Dashboard**: Boss role for content management

## 🛠️ Technology Stack

### Backend (Django)
- **Framework**: Django 5.2.3
- **API**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **Python Version**: 3.11

### Frontend (Next.js)
- **Framework**: Next.js 15.2.4
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.0
- **React Version**: 19.0.0
- **Build Tool**: Turbopack

## 📁 Project Structure

```
aptitude-website/
├── aptitude/                 # Django app
│   ├── models.py            # Database models
│   ├── views.py             # API views and web views
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL patterns
│   ├── backends.py          # Custom authentication backend
│   ├── templates/           # HTML templates
│   └── migrations/          # Database migrations
├── aptitude_prep/           # Django project settings
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL patterns
│   └── wsgi.py              # WSGI configuration
├── my-app/                  # Next.js frontend
│   ├── app/                 # App router directory
│   ├── public/              # Static assets
│   ├── package.json         # Node.js dependencies
│   └── next.config.ts       # Next.js configuration
├── manage.py                # Django management script
├── Pipfile                  # Python dependencies
└── README.md                # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn
- Git

### Backend Setup (Django)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Prathapkumar-67/aptitude-website.git
   cd aptitude-website
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install pipenv
   pipenv install
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start Django development server**
   ```bash
   python manage.py runserver
   ```

The Django backend will be available at `http://localhost:8000`

### Frontend Setup (Next.js)

1. **Navigate to frontend directory**
   ```bash
   cd my-app
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start Next.js development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

The Next.js frontend will be available at `http://localhost:3000`

## 📊 Database Models

### Core Models
- **User**: Custom user model with role-based access (Student/Boss)
- **Topic**: Main subject categories (Common, IT-specific, Govt-specific)
- **Subtopic**: Subdivisions within topics
- **VideoLesson**: Educational video content
- **Note**: Study materials and resources
- **Question**: Practice questions with difficulty levels
- **Option**: Multiple choice options for questions

### Tracking Models
- **UserAnswer**: Records user responses and performance
- **UserStreak**: Tracks daily learning consistency
- **NotificationSetting**: User notification preferences

## 🔗 API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/register/` - User registration
- `GET /api/me/` - Get current user info

### Content Management
- `GET /api/topics/` - List all topics
- `GET /api/subtopics/` - List subtopics
- `GET /api/lessons/` - Video lessons
- `GET /api/questions/` - Practice questions
- `GET /api/notes/` - Study materials

### User Progress
- `GET /api/streaks/` - User learning streaks
- `GET /api/notifications/` - Notification settings

## 🎨 Frontend Features

### Current Implementation
- Modern React 19 with Next.js 15
- TypeScript for type safety
- Tailwind CSS for responsive design
- App Router for optimal performance

### Planned Integrations
- API integration with Django backend
- User authentication flow
- Interactive question interface
- Progress visualization
- Real-time analytics dashboard

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/aptitude_db

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
```

### Production Deployment
- Configure PostgreSQL database
- Set up static file serving
- Configure CORS for frontend-backend communication
- Set up proper environment variables
- Use production-grade web server (Gunicorn + Nginx)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Prathap Kumar**
- GitHub: [@Prathapkumar-67](https://github.com/Prathapkumar-67)
- Project: [Aptitude Website](https://github.com/Prathapkumar-67/aptitude-website)

## 🙏 Acknowledgments

- Django REST Framework for robust API development
- Next.js team for the excellent React framework
- Tailwind CSS for beautiful, responsive design
- All contributors and users of this platform

---

⭐ **Star this repository if you find it helpful!**