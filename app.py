import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from utils import extract_text_from_pdf, clean_text, calculate_match
from gemini_helper import analyze_resume

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def is_allowed_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return render_template('results.html', score=0, ai_feedback='Please upload a resume PDF.'), 400

    file = request.files['resume']
    jd_text = request.form.get('job_description', '')

    if file.filename == '':
        return render_template('results.html', score=0, ai_feedback='Please select a resume PDF before analyzing.'), 400

    if not is_allowed_pdf(file.filename):
        return render_template('results.html', score=0, ai_feedback='Only PDF resume files are supported.'), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    resume_text = extract_text_from_pdf(file_path)

    resume_text = clean_text(resume_text)
    jd_text = clean_text(jd_text)

    if not resume_text:
        return render_template('results.html', score=0, ai_feedback='Could not extract readable text from this PDF. Please upload a text-based PDF resume.'), 400

    if not jd_text:
        return render_template('results.html', score=0, ai_feedback='Please enter a job description before analyzing.'), 400

    score = calculate_match(resume_text, jd_text)

    ai_feedback = analyze_resume(resume_text, jd_text)
    return render_template(
        'results.html',
        score=round(score, 2),
        ai_feedback=ai_feedback
    )

if __name__ == '__main__':
    app.run(debug=True)
