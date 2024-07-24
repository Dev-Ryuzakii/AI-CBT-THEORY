from flask import Flask, request, render_template, redirect, url_for
import joblib
import pandas as pd
from preprocessing import preprocess_text
from database import SessionLocal, Question, init_db

app = Flask(__name__)

# Load the model and vectorizers
model = joblib.load('models/marking_model.pkl')
vectorizer_student = joblib.load('models/vectorizer_student.pkl')
vectorizer_guide = joblib.load('models/vectorizer_guide.pkl')

@app.route('/')
def index():
    return redirect(url_for('student'))

@app.route('/questions', methods=['GET', 'POST'])
def manage_questions():
    session = SessionLocal()
    if request.method == 'POST':
        question_text = request.form['question_text']
        marking_guide = request.form['marking_guide']
        new_question = Question(question_text=question_text, marking_guide=marking_guide)
        session.add(new_question)
        session.commit()
        session.close()
        return redirect(url_for('manage_questions'))
    questions = session.query(Question).all()
    session.close()
    return render_template('manage_questions.html', questions=questions)

@app.route('/student', methods=['GET', 'POST'])
def student():
    session = SessionLocal()
    if request.method == 'POST':
        answer = request.form['answer']
        question_id = request.form['question_id']
        question = session.query(Question).filter_by(id=question_id).first()
        
        if not question:
            session.close()
            return "Question not found", 404
        
        processed_answer = preprocess_text(answer)
        processed_guide = preprocess_text(question.marking_guide)
        
        vectorized_answer = vectorizer_student.transform([processed_answer])
        vectorized_guide = vectorizer_guide.transform([processed_guide])
        
        X_combined = pd.concat([pd.DataFrame(vectorized_answer.toarray()), pd.DataFrame(vectorized_guide.toarray())], axis=1)

        if X_combined.shape[1] != model.n_features_in_:
            session.close()
            return f"Feature mismatch: model expects {model.n_features_in_} features, but got {X_combined.shape[1]}."

        score = model.predict(X_combined)[0]
        
        # Threshold for determining if the answer is correct
        threshold = 0.5
        is_correct = score > threshold
        
        session.close()
        return render_template('result.html', score=score, is_correct=is_correct)
    
    questions = session.query(Question).all()
    session.close()
    return render_template('student.html', questions=questions)

@app.route('/lecturer', methods=['GET', 'POST'])
def lecturer():
    if request.method == 'POST':
        question_text = request.form['question_text']
        marking_guide = request.form['marking_guide']
        
        new_question = Question(question_text=question_text, marking_guide=marking_guide)
        session = SessionLocal()
        session.add(new_question)
        session.commit()
        session.close()
        
        return redirect(url_for('lecturer'))
    return render_template('lecturer.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
