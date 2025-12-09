from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import ollama
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studybuddy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(100), default='General')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    review_count = db.Column(db.Integer, default=0)
    mastered = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class LearningSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flashcards_reviewed = db.Column(db.Integer, default=0, nullable=False)
    correct_count = db.Column(db.Integer, default=0, nullable=False)
    session_date = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id): return User.query.get(int(user_id))

def ask_ollama(prompt):
    try: return ollama.chat(model='phi', messages=[{'role':'user','content':prompt}])['message']['content']
    except: return "AI Error: Run 'ollama serve'"

def parse_flashcard_request(user_input):
    text = user_input.lower().strip()
    if any(k in text for k in ['create','make','add','new']) and any(k in text for k in ['flashcard','card']):
        for sep in ['about','on','for']:
            if sep in text:
                topic = text.split(sep,1)[1].strip()
                return {'question':f'What is {topic}?','answer':ask_ollama(f"Briefly explain {topic}")[:300],'category':topic.split()[0].capitalize() if topic.split() else 'General'}
    if '?' in user_input and len(user_input)<100:
        return {'question':user_input,'answer':ask_ollama(f"Brief answer:{user_input}")[:200],'category':'General'}
    return None

@app.route('/')
def home(): return redirect(url_for('login') if not current_user.is_authenticated else 'dashboard')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user); return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    total = Flashcard.query.filter_by(user_id=current_user.id).count()
    mastered = Flashcard.query.filter_by(user_id=current_user.id, mastered=True).count()
    recent = Flashcard.query.filter_by(user_id=current_user.id).order_by(Flashcard.created_date.desc()).limit(5).all()
    return render_template('dashboard.html', total_cards=total, mastered=mastered, recent_cards=recent)

@app.route('/chat', methods=['GET','POST'])
@login_required
def chat():
    ai_response, new_flashcard = "", None
    if request.method=='POST':
        user_message = request.form['message']
        flashcard_data = parse_flashcard_request(user_message)
        if flashcard_data:
            new_card = Flashcard(question=flashcard_data['question'], answer=flashcard_data['answer'], category=flashcard_data['category'], user_id=current_user.id)
            db.session.add(new_card); db.session.commit(); new_flashcard = flashcard_data
            ai_response = f"✅ Created flashcard: {flashcard_data['question'][:50]}..."
        else: ai_response = ask_ollama(user_message)
    return render_template('chat.html', ai_response=ai_response, new_flashcard=new_flashcard)

@app.route('/flashcards')
@login_required
def flashcards():
    cards = Flashcard.query.filter_by(user_id=current_user.id).all()
    return render_template('flashcards.html', flashcards=cards)

@app.route('/review/<int:card_id>/<result>')
@login_required
def review_card(card_id, result):
    card = Flashcard.query.get_or_404(card_id)
    if card.user_id != current_user.id: flash('Access denied'); return redirect(url_for('flashcards'))
    card.review_count = (card.review_count or 0) + 1
    if card.review_count >= 3: card.mastered = True
    today = datetime.utcnow().date()
    session = LearningSession.query.filter(LearningSession.user_id==current_user.id, db.func.date(LearningSession.session_date)==today).first()
    if not session: session = LearningSession(user_id=current_user.id); db.session.add(session)
    session.flashcards_reviewed = (session.flashcards_reviewed or 0) + 1
    if result == 'correct': session.correct_count = (session.correct_count or 0) + 1
    db.session.commit(); flash('Review recorded!'); return redirect(url_for('flashcards'))

@app.route('/delete_flashcard/<int:card_id>')
@login_required
def delete_flashcard(card_id):
    card = Flashcard.query.get_or_404(card_id)
    if card.user_id != current_user.id: flash('Access denied'); return redirect(url_for('flashcards'))
    db.session.delete(card); db.session.commit(); flash('Flashcard deleted!'); return redirect(url_for('flashcards'))

@app.route('/progress')
@login_required
def progress():
    sessions = LearningSession.query.filter_by(user_id=current_user.id).order_by(LearningSession.session_date.desc()).limit(10).all()
    total_reviews = sum(s.flashcards_reviewed or 0 for s in sessions)
    total_correct = sum(s.correct_count or 0 for s in sessions)
    accuracy = (total_correct / total_reviews * 100) if total_reviews > 0 else 0
    return render_template('progress.html', sessions=sessions, total_reviews=total_reviews, accuracy=accuracy)

@app.route('/logout')
@login_required
def logout(): logout_user(); return redirect(url_for('login'))

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password_hash=generate_password_hash('admin'))
            db.session.add(admin); db.session.commit()
            print("Created admin: admin/admin")

if __name__ == '__main__':
    init_db()
    print("Starting StudyBuddy AI...")
    app.run(debug=True)