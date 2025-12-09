# StudyBuddy AI - Local AI Learning Assistant

A Flask web application with local Ollama AI integration for creating and managing learning flashcards with natural language.

## Features
- 🔐 User authentication with bcrypt password hashing
- 🤖 Local Ollama AI (phi-2:2.7b) chatbot for learning assistance
- 📝 Natural language flashcard creation via AI chat
- 📊 Learning progress tracking and statistics
- 💾 SQLite database with SQLAlchemy ORM
- 🎨 Bootstrap 5 responsive interface
- 🚀 Ready for Render/Heroku deployment

## Prerequisites
1. Python 3.8+
2. Ollama installed locally
3. phi-2:2.7b model downloaded

## Installation

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd studybuddy-ai
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt