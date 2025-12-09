# StudyBuddy AI 🤖📚
## 🎮 Interactive Demo
**[Try the Static Demo Simulation](https://mea03kkw.github.io/studybuddy-ai/demo.html)** *(Simulates all features)*

*Note: Full application requires local setup (see below)*

## ✨ Features

### 🎯 Core Features
- **🤖 AI-Powered Flashcard Creation**: Create flashcards naturally by chatting with AI
- **🔐 Secure Authentication**: Bcrypt password hashing for safe login
- **📊 Learning Analytics**: Track study sessions and progress
- **🔄 Smart Review System**: Mark cards as correct/wrong to track mastery
- **🗑️ Easy Management**: Delete flashcards with one click
- **📱 Responsive Design**: Bootstrap 5 interface works on all devices
- **💬 Natural Language Interface**: "Create flashcard about Python" just works!

### 🚀 Technical Highlights
- **Local AI Integration**: Runs Ollama phi-2:2.7b model locally
- **Natural Language Processing**: Understands conversational flashcard requests
- **SQLite Database**: Lightweight database with SQLAlchemy ORM
- **Server-Side Rendering**: No JavaScript required - pure Flask templates
- **Under 200 Lines**: Clean, efficient codebase (app.py: 119 lines)

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Layer      │
│   ───────────   │    │   ───────────   │    │   ───────────   │
│ • Bootstrap 5   │◄──►│ • Flask         │◄──►│ • Ollama       │
│ • Jinja2        │    │ • SQLAlchemy    │    │ • phi-2:2.7b   │
│ • No custom JS  │    │ • Bcrypt        │    │ • Local Model   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                      ┌─────────────────┐
                      │   Database      │
                      │   ───────────   │
                      │ • SQLite        │
                      │ • 3 Models      │
                      └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed locally
- Git

## 📖 Usage Guide

### Creating Flashcards with AI
Simply chat naturally with the AI. Try these examples:
- **"Create a flashcard about Python lists"**
- **"Make a history card about World War 2"**
- **"Add math question: quadratic formula"**
- **"What is photosynthesis?"** (ends with ?)

The AI automatically detects these requests and creates flashcards!

### Reviewing Flashcards
1. Go to **Flashcards** page
2. For each card:
   - ✅ **Correct**: Mark as known
   - ❌ **Need Review**: Mark for later
3. After **3 correct reviews**, card is marked as **"Mastered"**

### Tracking Progress
- View **total reviews** and **accuracy rate**
- Track **study sessions** over time
- Monitor **mastered vs learning** cards

## 🗂️ Project Structure

```
studybuddy-ai/
├── app.py                    # Main Flask application (119 lines)
├── requirements.txt          # Python dependencies
├── Procfile                 # Heroku/Render deployment
├── render.yaml              # Render deployment config
├── .gitignore               # Git ignore rules
├── .env                     # Environment variables
├── demo.html                # Interactive demo simulation
│
├── templates/               # HTML templates
│   ├── base.html           # Base template with Bootstrap
│   ├── login.html          # Login page
│   ├── dashboard.html      # Main dashboard
│   ├── chat.html           # AI chat interface
│   ├── flashcards.html     # Flashcards management
│   └── progress.html       # Progress tracking
│
└── README.md               # This file
```

## 🔧 Technical Details

### Database Models
```python
User: id, username, password_hash
Flashcard: id, question, answer, category, created_date, review_count, mastered, user_id
LearningSession: id, user_id, flashcards_reviewed, correct_count, session_date
```

### Key Routes
- `/` → Redirect to login/dashboard
- `/login` → User authentication
- `/dashboard` → Learning statistics
- `/chat` → AI conversation interface
- `/flashcards` → Manage flashcards
- `/review/<id>/<result>` → Track reviews
- `/progress` → View learning analytics
- `/logout` → End session

### AI Integration
- Uses Ollama's **phi-2:2.7b** model locally
- Natural language processing for flashcard creation
- Fallback detection for reliable operation
- Error handling for Ollama connectivity

### Deployment Platforms
- **Render**: Use `render.yaml` configuration
- **Heroku**: Use `Procfile` configuration
- **PythonAnywhere**: Upload as Flask app

*Note: Ollama requires local installation, so AI features won't work on cloud platforms.*

This project demonstrates:
- **Full-stack Flask development**
- **Local AI model integration**
- **Database design with SQLAlchemy**
- **User authentication with bcrypt**
- **Natural language processing**
- **Bootstrap frontend development**
- **Project management within constraints**
