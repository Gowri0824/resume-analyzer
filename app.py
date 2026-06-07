from flask import Flask, render_template, request
import os
from utils import extract_text_from_pdf, clean_text, calculate_match
from gemini_helper import analyze_resume
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    jd_text = request.form['job_description']

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    resume_text = extract_text_from_pdf(file_path)

    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    score = calculate_match(resume_text, jd_text)

    ai_feedback = analyze_resume(resume_text, jd_text)
    return render_template(
    'result.html',
    score=round(score, 2),
    ai_feedback=ai_feedback
)

if __name__ == '__main__':
    app.run(debug=True)