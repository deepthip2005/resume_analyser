1. # Resume Analyzer & Job Match Recommendation System
2. Project Description

An NLP-powered system that parses resumes (PDF/DOCX), extracts skills and experience, and compares them with job descriptions. It generates a job-fit score, highlights missing skills, and provides personalized recommendations through an interactive Streamlit web app.

3. Features

Upload resume (PDF/DOCX).

Extract text and key skills automatically.

Paste or upload job description.

Get match percentage between resume & job.

View missing skills and suggestions to improve resume.

Simple, clean Streamlit interface.

4. Tech Stack

Python 3.10+

NLP Libraries: NLTK, Sentence Transformers

Machine Learning: scikit-learn, TF-IDF

File Parsing: PyPDF2, python-docx

Frontend: Streamlit

5. Installation
# Clone the repo
git clone <your-repo-url>
cd resume-analyzer

# Install dependencies
pip install -r requirements.txt

6. Usage
# Run backend functions
python matcher.py

# Launch the web app
streamlit run app.py

